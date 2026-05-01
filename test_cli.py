# Math/tests/test_cli.py
"""
Tests that verify the command‑line interface (`main.py`) behaves as expected.

The tests:

1. Run the script with an equation passed as a positional argument.
2. Run the script without arguments and feed the equation via *stdin*.
3. Check that the output contains the four expected steps:
   – original LaTeX, simplified LaTeX, symbolic solution(s), numeric approximation(s).
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

# Path to the project root (one level up from the test file)
PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _run_cli(
    args: list[str], input_text: str | None = None
) -> subprocess.CompletedProcess:
    """Utility that runs `main.py` with the supplied arguments.

    The function uses the same interpreter that runs the tests
    (`sys.executable`) and executes the script from the project root,
    ensuring that relative imports work correctly.
    """
    cmd = [sys.executable, str(PROJECT_ROOT / "main.py")] + args
    return subprocess.run(
        cmd,
        input=input_text,
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT,
        timeout=5,
    )


def _strip_spaces(s: str) -> str:
    """Remove whitespace that is irrelevant for LaTeX comparison."""
    return "".join(s.split())


def test_cli_argument_passed():
    """Pass the equation as a CLI argument."""
    result = _run_cli(["x^2 - 5x + 6 = 0"])
    assert result.returncode == 0, f"CLI failed: {result.stderr}"
    lines = [_strip_spaces(line) for line in result.stdout.strip().splitlines()]
    # The script should produce exactly four lines.
    assert len(lines) == 4
    # Original equation must appear unchanged (ignoring whitespace).
    assert lines[0] == _strip_spaces("x^2 - 5x + 6 = 0")
    # Symbolic part must contain both solutions.
    assert "x=2" in lines[2] and "x=3" in lines[2]


def test_cli_stdin():
    """Pass the equation via stdin (no positional argument)."""
    result = _run_cli([], input_text="x^2 - 5x + 6 = 0")
    assert result.returncode == 0, f"CLI failed: {result.stderr}"
    lines = [_strip_spaces(line) for line in result.stdout.strip().splitlines()]
    assert len(lines) == 4
    assert lines[0] == _strip_spaces("x^2 - 5x + 6 = 0")
    assert "x=2" in lines[2] and "x=3" in lines[2]
