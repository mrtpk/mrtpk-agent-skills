"""<Write-up title> - part <NN>: <topic>.

Every measured number in part <NN> comes from the output of this script.
Run: uv run --with numpy python scripts/<NN>_<slug>.py
"""

import numpy as np


def section(title: str, seed: int) -> np.random.Generator:
    """Print a section header and give the section its own RNG.

    A fixed seed per section keeps the numbers of a section stable
    when another section is added or changed.
    """
    print(f"\n== {title} ==")
    return np.random.default_rng(seed)


def report(what: str, value: object, expected: object) -> None:
    """Print one check line: what is checked, the value, the expected value and the result."""
    status = "OK" if value == expected else "DIFFERENT"
    print(f"{what}: {value} (expected {expected}) -> {status}")


def main() -> None:
    rng = section("1. <first idea>", seed=1)
    x = rng.normal(size=1000)
    clipped = np.clip(x, -2.0, 2.0)
    # Deliberate counter-example: about 4.6 % of normal samples lie outside [-2, 2], so this prints DIFFERENT.
    report("values changed by the clip", int(np.sum(clipped != x)), 0)

    rng = section("2. <second idea>", seed=2)
    # ...


if __name__ == "__main__":
    main()
