# Math/tests/test_engine.py
"""
Pytest test suite for the LaTeX equation solving engine.

The tests cover:
* Solving a single quadratic equation.
* Solving a simple linear system of equations.
* Proper handling of malformed input (error reporting).
"""

from __future__ import annotations

import re

import pytest

from engine import generate_solution_steps


def _strip_latex_spaces(s: str) -> str:
    """Utility to remove whitespace that is not significant for LaTeX comparison."""
    return re.sub(r"\s+", "", s)


def test_quadratic_equation_steps():
    """A quadratic equation should yield original, simplified, symbolic, and numeric steps."""
    latex_input = r"x^2 - 5x + 6 = 0"
    steps = generate_solution_steps(latex_input)

    # Expect exactly 4 steps (original, simplified, symbolic, numeric)
    assert len(steps) == 4

    # Step 0 – original input should be unchanged (ignoring surrounding whitespace)
    assert _strip_latex_spaces(steps[0]) == _strip_latex_spaces(latex_input)

    # Step 1 – simplified form (SymPy may reorder terms)
    # We only check that the simplified expression still contains the same symbols.
    assert "x" in steps[1]
    assert "=" in steps[1]

    # Step 2 – symbolic solutions (e.g. x = 2, x = 3)
    assert "x=2" in _strip_latex_spaces(steps[2]) or "x = 2" in steps[2]
    assert "x=3" in _strip_latex_spaces(steps[2]) or "x = 3" in steps[2]

    # Step 3 – numeric approximations (should be close to the symbolic ones)
    numeric_clean = _strip_latex_spaces(steps[3])
    assert "x\\approx2." in numeric_clean
    assert "x\\approx3." in numeric_clean


def test_linear_system_steps():
    """A simple 2×2 linear system should be solved correctly."""
    latex_input = r"""
        \begin{cases}
            x + y = 3 \\
            2x - y = 0
        \end{cases}
    """
    steps = generate_solution_steps(latex_input)

    # At minimum we should receive four steps as before.
    assert len(steps) >= 4

    # Symbolic solution should contain both variables.
    symbolic = _strip_latex_spaces(steps[2])
    assert "x=1" in symbolic or "x = 1" in steps[2]
    assert "y=2" in symbolic or "y = 2" in steps[2]

    # Numeric step should approximate the same values.
    numeric = _strip_latex_spaces(steps[3])
    assert "x\\approx1." in numeric
    assert "y\\approx2." in numeric


def test_malformed_input_error():
    """When the input cannot be parsed, the engine should return a single LaTeX error block."""
    malformed = "this is not a valid latex equation"
    steps = generate_solution_steps(malformed)

    # The engine returns a list with one element containing the error.
    assert isinstance(steps, list)
    assert len(steps) == 1

    error_block = steps[0]
    # The error block should contain the word "Error" in LaTeX form.
    assert r"\text{Error:}" in error_block or "Error" in error_block


def test_complex_roots():
    """Complex solutions should be returned correctly (e.g., x^2 + 1 = 0)."""
    latex_input = r"x^2 + 1 = 0"
    steps = generate_solution_steps(latex_input)

    # Expect four steps: original, simplified, symbolic, numeric.
    assert len(steps) == 4

    # Symbolic step must contain the imaginary unit I.
    symbolic = _strip_latex_spaces(steps[2])
    # Symbolic step should contain the imaginary unit (SymPy may render as \"i\" or \"I\").\n    assert \"i\" in symbolic.lower()

    # Numeric approximation should also contain I.
    numeric = _strip_latex_spaces(steps[3])
    # Numeric approximation should also contain the imaginary unit.\n    assert \"i\" in numeric.lower()
