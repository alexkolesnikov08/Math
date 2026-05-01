# Math Equation Solver

A compact Python utility that parses mathematical equations written in LaTeX, solves them both symbolically and numerically, and returns a step‑by‑step solution in LaTeX format.

## Features

- Supports single equations and systems of equations.
- Symbolic simplification, solving, and numeric approximation.
- Full LaTeX output (original input, simplified form, symbolic solution, numeric approximation).
- Command‑line interface (`main.py`) and importable engine (`engine.py`).
- Powered by **SymPy** – no external mathematics engines required.

## Installation

1. **Clone the repository** (or copy the files into your project):

   ```bash
   git clone https://github.com/alexkolesnikov08/Math
   cd Math
   ```

2. **Install the required dependencies** for the interpreter you plan to use. The
   project provides a `requirements.txt` that fixes the versions required by
   the LaTeX parser (`sympy≥1.12` and `antlr4-python3-runtime==4.11`).

   ```bash
   # Homebrew‑installed Python 3.11 on macOS
   /opt/homebrew/bin/python3.11 -m pip install --upgrade pip
   /opt/homebrew/bin/python3.11 -m pip install -r requirements.txt
   ```

   If you prefer an isolated environment, create a virtualenv **with the same
   interpreter** and install from `requirements.txt` inside it.

3. **Make the CLI executable (optional).** `main.py` now starts with a shebang
   that points to the interpreter above, so you can run it directly:

   ```bash
   chmod +x main.py
   ./main.py "x^2 - 5x + 6 = 0"
   ```

   > The code works with Python 3.10+ but the shebang guarantees it runs with the
   > interpreter you installed the dependencies for.

## Usage

### As a CLI tool

Run the solver directly via the module entry point:

```bash
# Pass the equation as an argument
python -m Math.main "x^2 - 5x + 6 = 0"

# Or pipe the equation via stdin
echo "x^2 - 5x + 6 = 0" | python -m Math.main
```

The program prints each solution step on a separate line, e.g.:

```
x^2 - 5x + 6 = 0
x^{2} - 5 x + 6 = 0
x = 2,\; x = 3
x \approx 2.00000000000000,\; x \approx 3.00000000000000
```

### As a library

Import the engine in your own Python code:

```python
from engine import generate_solution_steps

latex_eq = r"\begin{cases} x + y = 3 \\ 2x - y = 0 \end{cases}"
steps = generate_solution_steps(latex_eq)

for step in steps:
    print(step)
```

The returned `steps` list contains LaTeX strings representing each stage of the solution.

## Project Structure

```
Math/
├── engine.py      # Core solving logic (importable)
├── main.py        # CLI entry point
├── README.md      # You are reading it now
└── documentation.md  # Detailed engine documentation
```

## Contributing

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/my‑feature`).
3. Ensure code follows **Google Python Style Guide** and passes linting.
4. Submit a pull request with a clear description of the changes.

## License

This project is released under the MIT License. Feel free to use, modify, and distribute it.

---  
*Generated on 2026‑05‑01 by the Math Equation Solver project.*
