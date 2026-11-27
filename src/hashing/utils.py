"""Module containing hashing functions that might be used accros many other
modules"""

import numpy as np
import galois

gf2 = galois.GF(2)


# TODO : optimize
def get_random_toeplitz_matrix(
    rng: np.random.Generator,
    nb_rows: int,
    nb_cols: int,
) -> galois.FieldArray:
    """Computes a random Toeplitz matrix for hashing purposes

    :param rng: The random number generator to use
    :type rng: np.random.Generator
    :param nb_rows: The number of rows the Toeplitz matrix will need to
        have
    :type nb_rows: int
    :param nb_cols: The number of columns the Toeplitz matrix will need to
        have
    :type nb_cols: int
    :return: The random Toeplitz matrix
    :rtype: galois.FieldArray
    """
    values = rng.integers(0, 2, size=nb_cols + nb_rows - 1)

    matrix = np.zeros(shape=(nb_rows, nb_cols), dtype=np.uint8)
    for i in range(nb_rows):
        for j in range(nb_cols):
            matrix[i, j] = values[nb_cols - 1 + i - j]

    return gf2(matrix)


def convert_list_to_gf2(l: list[int]) -> galois.FieldArray:
    """Converts a binary list to a GF(2) representation

    :param l: The list to convert. Must contain only 0s and 1s.
    :type l: list[int]
    :return: The string converted to GF(2)
    :rtype: galois.FieldArray"""
    return gf2(l)


def convert_string_to_gf2(s: str) -> galois.FieldArray:
    """Converts a binary string to a GF(2) representation

    :param s: The string to convert
    :type s: str
    :return: The string converted to GF(2)
    :rtype: galois.FieldArray"""

    return convert_list_to_gf2([int(c, 2) for c in s])
