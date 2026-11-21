"""Names of parameters of different classes"""

from enum import StrEnum, auto


class CascadeParams(StrEnum):
    """The names of the different parameters for the Cascade"""

    SEED = auto()
    NUMBER_OF_PASSES = auto()
    ALPHA = auto()
    BETA = auto()
    IDX_PASS_FORCE_SIZE = auto()
