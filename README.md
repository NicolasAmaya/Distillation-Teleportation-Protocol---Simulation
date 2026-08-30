# Boolean Table Correction Simulation

This Python program simulates repeatedly correcting a randomly generated Boolean function table. On each iteration, it generates a random error value `m`, shifts the current table using `x XOR m`, and combines the two tables using

```text
f'(x) = f(x) XOR f(x XOR m)
```

The simulation stops when every entry in the table is equal. A table containing only `0`s or only `1`s represents a degree-0 (constant) Boolean function.

## Requirements

- Python 3

The program uses only Python's built-in `random` module. NumPy and other third-party packages are not required.

## Running the simulation

Save the simulation as a Python file, for example `simulation.py`, and run:

```bash
python3 simulation.py
```

The default value in `main()` is:

```python
qubits = 3
```

This creates a table with `2 ** 3`, or 8, entries. Change `qubits` to simulate a different table size.

## How it works

1. The program creates a random Boolean table with `2 ** qubits` entries.
2. While the table is not constant, it generates a random `qubits`-bit integer `m`.
3. It produces a shifted table whose entry at index `x` is the current table's entry at index `x XOR m`.
4. It creates the next table by XORing corresponding entries of the current and shifted tables.
5. It repeats until all table entries are `0` or all entries are `1`.

Because `m` is chosen randomly, the number of iterations and the intermediate tables can differ each time the program runs.

## Functions

### `main()`

Controls the simulation. It sets the number of qubits to 3, generates the initial table, repeatedly applies the correction operation, and prints the values produced during each iteration. The loop ends when `isCorrect()` reports that the table is constant.

### `genTable(qubits)`

Generates a random Boolean function table containing `2 ** qubits` entries. Each entry is independently chosen as either `0` or `1`.

The function also formats each index as a binary string in `bitstr`. In the supplied code, that variable is not used after it is created.

### `genM(qubits)`

Generates a random `qubits`-bit integer `m` one bit at a time. This value represents the randomly selected error or shift used in the current iteration.

For three qubits, `m` can range from 0 through 7.

### `genVf(table)`

Converts each Boolean table entry into a phase value using

```text
(-1) ** entry
```

This maps `0` to `1` and `1` to `-1`. The current `main()` function does not call `genVf()`, but it can be used to represent the diagonal values of the corresponding `Vf` operation.

### `shiftTable(table, m)`

Creates the shifted table:

```text
shifted[x] = table[x XOR m]
```

Python's `^` operator performs the bitwise XOR operation.

### `correctionTable(table, m)`

First calls `shiftTable()` and then XORs each original entry with the matching shifted entry:

```text
nextTable[x] = table[x] XOR table[x XOR m]
```

This implements the correction update `f'(x) = f(x) XOR f(x XOR m)`.

### `isCorrect(table)`

Returns `True` when every entry equals the first entry in the table. This means the result is constant—either all `0`s or all `1`s—and the degree-0 stopping condition has been reached.

## Understanding the output

Each loop iteration prints:

- `Iteration`: the iteration number, beginning at 0.
- `error m`: the randomly generated shift/error value.
- `Current Table`: the table before correction.
- `Shifted Table`: the values of the current table reordered using `x XOR m`.
- `Next Table`: the entry-by-entry XOR of the current and shifted tables.

The program also prints `Final Table`, showing the updated table. In the supplied indentation, this print statement appears inside the loop, so it is printed after every correction rather than only once after the loop finishes.

Example output structure:

```text
Iteration 0:
error m = 3
[1, 0, 1, 1, 0, 0, 1, 0] - Current Table
[1, 1, 0, 1, 0, 1, 0, 0] - Shifted Table
[0, 1, 1, 0, 0, 1, 1, 0] - Next Table
Final Table: [0, 1, 1, 0, 0, 1, 1, 0]
```

The exact values will vary because the initial table and `m` are random.

