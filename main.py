#!/opt/homebrew/bin/python3.11
# Math/main.py
"""
Command‑line interface for the LaTeX equation solver.

Usage:
    python -m Math.main "x^2 - 5x + 6 = 0"
    echo "x^2 - 5x + 6 = 0" | python -m Math.main

The script reads a LaTeX string representing one equation or a system,
passes it to :func:`engine.generate_solution_steps`, and prints each
solution step on a separate line.
"""

from __future__ import annotations

import argparse
import sys

from engine import generate_solution_steps


def _parse_arguments() -> argparse.Namespace:
    """Parse command‑line arguments."""
    parser = argparse.ArgumentParser(
        description="Solve LaTeX equations and output a step‑by‑step LaTeX solution."
    )
    parser.add_argument(
        "equation",
        nargs="?",
        help=(
            "LaTeX string of the equation or system to solve. "
            "If omitted, the script reads from standard input."
        ),
    )
    return parser.parse_args()


def main() -> None:
    """Entry point for the CLI utility."""
    args = _parse_arguments()

    # Obtain the raw LaTeX input.
    if args.equation:
        raw_input = args.equation
    else:
        # Read everything from stdin (allow multi‑line input).
        raw_input = sys.stdin.read().strip()

    if not raw_input:
        sys.stderr.write("Error: No equation provided.\n")
        sys.exit(1)

    # Generate solution steps using the engine.
    steps = generate_solution_steps(raw_input)

    # Print each step on its own line.  Users can redirect the output or pipe it
    # into other tools that understand LaTeX.
    for step in steps:
        print(step)


if __name__ == "__main__":
    main()
