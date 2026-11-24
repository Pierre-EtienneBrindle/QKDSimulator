"""Module containing utility functions for QKD protocols"""

import numpy as np


def binary_entropy(prob: float) -> float:
    """
    The binary entropy function. When p >= .5, it always returns 1

    :param prob: The probability
    :type prob: float
    :return: The entropy
    :rtype: float
    """
    if prob < 0:
        raise ValueError("Invalide probability")
    if prob == 0:
        return 0
    if prob >= 0.5:
        return 1
    return -(np.log2(prob) * prob + (1 - prob) * np.log2(1 - prob))
