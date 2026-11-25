"""Module containing the name of parameters for different privacy
amplification protocol"""

from enum import StrEnum, auto


class ToeplitzAmpParams(StrEnum):
    """The parameters of the Toeplitz matrix based extractor"""

    SEED = auto()
