# <Write-up title>

<Two to four sentences: what the system is, who the readers are, what the write-up answers.>

Source: <repository URL> at commit `<hash>` (internal mode only).

## Parts

| Part | Question it answers |
|---|---|
| [01. <topic>](01-<slug>.md) | <question> |
| [NN. Gaps and lessons](NN-<slug>.md) | what held up, the gaps, what to change |

## Re-run the checks

```
uv run --with numpy python scripts/01_<slug>.py
```

## Rebuild the figures

```
PYTHONDONTWRITEBYTECODE=1 uv run --with cairosvg --with numpy python tools/build_figures.py .
```

Install the Inter font and a monospace font (Menlo, Consolas or SFMono), so that the PNG text matches the SVG.
