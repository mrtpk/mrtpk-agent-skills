"""Trigger eval (level 3): does each skill start for the right requests, and stay off for the others?

Usage:
    python3 trigger_eval.py <skills dir> [--skill NAME ...] [--runs 3] [--max-calls 5] [--jobs 4]
                            [--timeout 180] [--model ID] [--dry-run]

Input: <skills dir>/<skill>/evals/trigger_evals.json, a list of
    {"query": "...", "should_trigger": true|false}
Each query runs `claude -p` once per repeat, in its own empty folder. The skills load as a plugin named "team"
(--plugin-dir) under --restricted and --strict-mcp-config, so user-level skills, user settings and MCP connectors do
not load. A run stops at the first Skill call, after --max-calls tool calls, or at the end of the reply.

A run is correct when (the first Skill call is team:<name>) == should_trigger.
A query passes only when all its runs are correct. A run that fails (exit code, error result, no start, timeout) is
ERROR, never correct. Exit code: 0 all pass, 1 a query fails, 2 a run had an error.
Skills with `disable-model-invocation: true` are skipped: only their slash command starts them.
Cost: one short claude run per query and repeat, on the user's normal usage. Use --dry-run to see the count.
"""

import argparse
import concurrent.futures as cf
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
from pathlib import Path

PLUGIN = "team"
DENY = ["Bash", "Write", "Edit", "NotebookEdit", "Agent", "Task", "WebFetch", "WebSearch"]


def front_matter(skill_md: Path) -> dict[str, str]:
    text = skill_md.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    out: dict[str, str] = {}
    for line in (m.group(1) if m else "").splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip()
    return out


def check_cli() -> str | None:
    """Return an error text when the claude CLI is absent or lacks a flag that the runner needs."""
    if not shutil.which("claude"):
        return "the claude CLI is not on PATH"
    out = subprocess.run(["claude", "--help"], capture_output=True, text=True, timeout=60).stdout
    missing = [f for f in ("--restricted", "--strict-mcp-config", "--plugin-dir") if f not in out]
    if missing:
        return f"claude --help does not list {', '.join(missing)}; the runner cannot isolate the skills"
    return None


def build_plugin(skills: list[Path], root: Path) -> Path:
    plug = root / "plugin"
    (plug / ".claude-plugin").mkdir(parents=True)
    (plug / ".claude-plugin" / "plugin.json").write_text(json.dumps({"name": PLUGIN, "version": "0.0.0"}))
    for s in skills:
        shutil.copytree(s, plug / "skills" / s.name, ignore=shutil.ignore_patterns("evals", "__pycache__"))
    return plug


def one_run(query: str, plug: Path, args: argparse.Namespace) -> tuple[str, str]:
    """Return (outcome, detail). Outcome: a skill name, "-" (no skill), or "ERROR"."""
    cmd = ["claude", "-p", query, "--restricted", "--strict-mcp-config", "--plugin-dir", str(plug),
           "--output-format", "stream-json", "--verbose", "--allowedTools", "Skill", "--disallowedTools", *DENY]
    if args.model:
        cmd += ["--model", args.model]
    with tempfile.TemporaryDirectory(prefix="trig-") as cwd:
        p = subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                             start_new_session=True)
        timed_out = threading.Event()

        def kill() -> None:
            try:
                os.killpg(p.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass

        def on_timeout() -> None:
            timed_out.set()
            kill()

        timer = threading.Timer(args.timeout, on_timeout)
        timer.start()
        calls: list[str] = []
        started = False
        result_error = None
        found = None
        try:
            assert p.stdout is not None
            for line in p.stdout:
                try:
                    ev = json.loads(line)
                except ValueError:
                    continue
                if ev.get("type") == "system" and ev.get("subtype") == "init":
                    started = True
                elif ev.get("type") == "assistant":
                    for c in ev["message"].get("content", []):
                        if c.get("type") != "tool_use":
                            continue
                        if c["name"] == "Skill":
                            found = str(c["input"].get("skill", ""))
                            break
                        calls.append(c["name"])
                    if found is not None or len(calls) >= args.max_calls:
                        break
                elif ev.get("type") == "result":
                    if ev.get("is_error"):
                        result_error = str(ev.get("result") or ev.get("subtype"))[:200]
                    break
        finally:
            timer.cancel()
            kill()
            p.wait()
            err = (p.stderr.read() if p.stderr else "")[-300:]
        if timed_out.is_set():
            return "ERROR", f"timeout after {args.timeout}s"
        if found is not None:
            return found, ""
        if not started:
            return "ERROR", f"no start; stderr: {err.strip()}"
        if result_error:
            return "ERROR", result_error
        return "-", "/".join(calls)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("skills_dir", type=Path)
    ap.add_argument("--skill", action="append", default=[], help="test only the queries of this skill (repeatable)")
    ap.add_argument("--runs", type=int, default=3)
    ap.add_argument("--max-calls", type=int, default=5)
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--timeout", type=int, default=180, help="seconds per run")
    ap.add_argument("--model")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    skills, cases = [], []
    found: set[str] = set()
    # Skills at the top level and one level down (for example skills/work/<skill>).
    skill_mds = sorted(set(args.skills_dir.glob("*/SKILL.md")) | set(args.skills_dir.glob("*/*/SKILL.md")))
    folders = [m.parent.name for m in skill_mds]
    dupes = sorted({f for f in folders if folders.count(f) > 1})
    if dupes:
        print(f"ERROR: two skill folders have the same name: {', '.join(dupes)}")
        return 2
    for skill_md in skill_mds:
        fm = front_matter(skill_md)
        name = fm.get("name", skill_md.parent.name)
        found.add(name)
        if fm.get("disable-model-invocation", "").lower() == "true":
            print(f"skip {name}: disable-model-invocation")
            continue
        # Load every skill, so that siblings compete for near-miss queries. --skill filters only the queries.
        skills.append(skill_md.parent)
        if args.skill and name not in args.skill:
            continue
        ev = skill_md.parent / "evals" / "trigger_evals.json"
        if ev.exists():
            cases += [(name, q) for q in json.loads(ev.read_text(encoding="utf-8"))]
        else:
            print(f"skip {name}: no evals/trigger_evals.json")
    for name in sorted(set(args.skill or []) - found):
        print(f"WARN --skill {name}: no skill with this name in {args.skills_dir}")
    total = len(cases) * args.runs
    print(f"{len(skills)} skills loaded, {len(cases)} queries x {args.runs} runs = {total} claude runs")
    if args.dry_run or not cases:
        return 0
    problem = check_cli()
    if problem:
        print(f"ERROR: {problem}")
        return 2

    root = Path(tempfile.mkdtemp(prefix="trigger-eval-"))
    try:
        plug = build_plugin(skills, root)
        jobs = [i for i in range(len(cases)) for _ in range(args.runs)]
        got: dict[int, list[tuple[str, str]]] = {i: [] for i in range(len(cases))}
        with cf.ThreadPoolExecutor(args.jobs) as ex:
            futs = {ex.submit(one_run, cases[i][1]["query"], plug, args): i for i in jobs}
            for f in cf.as_completed(futs):
                got[futs[f]].append(f.result())
    except KeyboardInterrupt:
        print("interrupted")
        return 2
    finally:
        shutil.rmtree(root, ignore_errors=True)

    per: dict[str, list[int]] = {}
    errors = 0
    for i, (name, c) in enumerate(cases):
        want = bool(c["should_trigger"])
        outs = got[i]
        errors += sum(o == "ERROR" for o, _ in outs)
        correct = sum(o != "ERROR" and (o == f"{PLUGIN}:{name}") == want for o, _ in outs)
        ok = correct == args.runs
        per.setdefault(name, [0, 0])
        per[name][0] += ok
        per[name][1] += 1
        shown = ",".join(o if o != "ERROR" else f"ERROR({d})" for o, d in outs)
        print(f"{'PASS' if ok else 'FAIL'} {correct}/{args.runs} {name:26} want={'yes' if want else 'no '} "
              f"got={shown} | {c['query'][:70]}")
    print()
    for name, (p, n) in per.items():
        print(f"{name:26} {p}/{n} queries pass")
    passed = sum(p for p, _ in per.values())
    print(f"TOTAL {passed}/{len(cases)} queries pass all {args.runs} runs; {errors} run error(s)")
    if errors:
        return 2
    return 0 if passed == len(cases) else 1


if __name__ == "__main__":
    sys.exit(main())
