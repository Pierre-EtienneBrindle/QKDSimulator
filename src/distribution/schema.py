"""Names of parameters of different classes"""

from enum import StrEnum, auto


class DepolarizingParams(StrEnum):
    """Names of the parameters of the single qbit depolarizing channel"""

    PROBABILITY = auto()


class AmplitudeDampingParams(StrEnum):
    """Names of the parameters of the single qbit amplitude damping
    channel"""

    PROBABILITY = auto()


class BB84Params(StrEnum):
    """Names of the parameters of the BB84 key distribution protocol"""

    MAX_ERROR_RATE = auto()
    TARGET_KEY_SIZE = auto()
    RANDOM_SEED = auto()


class BB84QbitLabels(StrEnum):
    """Names of the qbit in the BB84 key distribution protocol"""

    ALICE_BIT_CHOICE = auto()
    ALICE_BASE_CHOICE = auto()
    TRANSMITTED = auto()
    BOB_BASE_CHOICE = auto()


class TomamichelEtAlParams(StrEnum):
    """Names of the parameters of the Tomamichel et al. QKD protocol"""

    MAX_ERROR_RATE = auto()
    BLOC_SIZE = auto()
    DETECTION_SIZE = auto()
    RANDOM_SEED = auto()


class TomamichelEtAlQbitLabels(StrEnum):
    """Names of the different qubit of the Tomamichel et al. QKD protocol"""

    ALICE_BIT_CHOICE = auto()
    ALICE_BASE_CHOICE = auto()
    TRANSMITTED = auto()
    BOB_BASE_CHOICE = auto()
