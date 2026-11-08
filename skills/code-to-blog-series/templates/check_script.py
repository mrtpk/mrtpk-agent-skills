"""<Series> - Part <N>: <topic>.

Every number in the post comes from the output of this script.
Run: uv run --with numpy python <slug>.py
"""

import numpy as np


def section(title: str, seed: int) -> np.random.Generator:
    """Print a section header and give the section its own RNG.

    A fixed seed per section keeps the numbers of a section stable
    when another section is added or changed.
    """
    print(f"\n== {title} ==")
    return np.random.default_rng(seed)


def main() -> None:
    rng = section("1. <first idea>", seed=1)
    x = rng.integers(-128, 128, size=1000)
    ok = bool(np.all(x >= -128))
    print("<what is checked>. Is pass?", ok)

    rng = section("2. <second idea>", seed=2)
    # ...


if __name__ == "__main__":
    main()
