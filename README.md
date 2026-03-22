# Rectangular Finite Quantum Well
## One-Dimensional Stationary Schrödinger Equation

A Python project for the numerical solution of the stationary Schrödinger equation for a one-dimensional rectangular finite quantum well.

Detailed numerical results can be found in the file `results/wyniki.md`.

## Project Contents

### `src/studnia4.py`
Program implementing Task 1:
- tabulation of the functions `F_even(ε)` and `F_odd(ε)`,
- determination of zero points corresponding to energy levels,
- analysis of various potential well parameters,
- generation of graphs.

### `src/atom_1.py`
Program implementing Task 2 and Advanced Task 1:
- fitting the quantum well parameters to the first energy levels of the hydrogen atom,
- analyzing the consistency of the results,
- automatically finding the well parameters.

### `src/atom2.py`
Program implementing Advanced Task 2:
- determination of eigenfunctions,
- plotting eigenfunctions and `|ψ|²`,
- observation of quantum tunneling.

## Requirements

The project uses the following libraries:
- NumPy
- SciPy
- Matplotlib

Installation:
```bash
pip install -r requirements.txt
