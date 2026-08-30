"""
QRAM Teleportation Correction Simulation

This program simulates the correction procedure required after
teleporting a QRAM phase-oracle resource state V_f.

The simulation:
    1. Generates a random Boolean function f(x) to represent the
       QRAM table used for the simulation.
    2. Simulates a teleportation error X^m by generating m.
    3. Computes the shifted function f(x XOR m).
    4. Computes the required correction function:
           f'(x) = f(x) XOR f(x XOR m)
    5. Repeats the correction procedure recursively until the
       correction function is constant.

The random function f(x) is part of the simulated QRAM data and is
generated before teleportation. Teleportation introduces the error m,
not the function f(x).

Reference:
    A. M. Dalzell et al.,
    "A distillation-teleportation protocol for fault-tolerant QRAM,"
    arXiv:2505.20265v1 [quant-ph], 2025.

Next Steps:
    - Implement the quantum circuit in PennyLane.
    - Apply the computed correction to the live quantum state.
    - Verify that the corrected state matches the expected V_f|psi> state.

Author: Nicolas Amaya
Last Edited: 2026-08-30


"""
import random


def main():
    # Number of address qubits.
    # The table therefore contains 2^qubits entries.
    qubits = 3

    # Generate the original Boolean function f(x).
    originalTable = genTable(qubits)

    # currTable represents the function being corrected at the current
    # iteration. Keep originalTable unchanged for later verification.
    currTable = originalTable.copy()

    count = 0

    # Repeatedly generate correction functions until the current
    # function has degree 0 (all table entries are equal).
    while not isCorrect(currTable):

        print(f"Iteration {count}:")

        # Simulate a random X^m teleportation error.
        m = genM(qubits)

        # Compute the shifted function:
        #     f(x XOR m)
        st = shiftTable(currTable, m)

        # Compute the correction function:
        #     f'(x) = f(x) XOR f(x XOR m)
        nextTable = correctionTable(currTable, m)

        print(f"error m = {m}")
        print(f"{currTable} - Current Table")
        print(f"{st} - Shifted Table")
        print(f"{nextTable} - Next Table")

        # The correction function becomes the function used
        # in the next recursive correction step.
        currTable = nextTable
        count += 1

    print("Final Table: {}".format(currTable))


def genTable(qubits: int):
    """
    Generates a random truth table for a Boolean function

        f : {0,1}^n -> {0,1}

    where n is the number of address qubits.
    """

    table = list()

    # An n-qubit address register contains 2^n possible addresses.
    for i in range(2 ** qubits):

        # Binary representation of the address.
        bitstr = format(i, f"0{qubits}b")

        # Assign a random value f(x) in {0,1} to this address.
        table.append(random.randint(0, 1))

    return table


def genM(qubits: int):
    """
    Generates a random n-bit teleportation error m.

    The integer m represents the bit string specifying which
    address qubits received an X correction.
    """

    for i in range(0, qubits):

        bit = random.randint(0, 1)

        # Build the binary value of m one bit at a time.
        if i > 0:
            m = (m << 1) | bit
        else:
            m = bit

    return m


def genVf(table: list):
    """
    Converts the Boolean truth table f(x) into the diagonal entries
    of the phase oracle V_f:

        V_f |x> = (-1)^f(x) |x>

    Therefore:
        f(x) = 0 -> +1
        f(x) = 1 -> -1
    """

    return [(-1)**entry for entry in table]

    # If NumPy is later used, the full V_f matrix could be constructed as:
    # return np.diag(diagonal)


def shiftTable(table: list, m):
    """
    Computes the truth table of the shifted function

        f(x XOR m)

    XORing the address x with m determines which original
    table entry corresponds to each shifted address.
    """

    return [table[x ^ m] for x in range(len(table))]


def correctionTable(table: list, m):
    """
    Computes the correction function

        f'(x) = f(x) XOR f(x XOR m)

    This corresponds to the phase correction required after
    the X^m teleportation error.
    """

    # Truth table for f(x XOR m).
    st = shiftTable(table, m)

    # XOR the function values, not the addresses:
    #
    #     f'(x) = f(x) XOR f(x XOR m)
    #
    return [x ^ y for x, y in zip(table, st)]


def isCorrect(table: list):
    """
    Tests whether the current correction function has reached
    degree 0.

    A degree-0 Boolean function is constant, so its truth table
    must contain either all 0s or all 1s.
    """

    return all([value == table[0] for value in table])


if __name__ == "__main__":
    main()