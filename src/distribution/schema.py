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


class BB84EveParams(StrEnum):
    """Parameters of Eve when attacking the BB84 key distribution protocol"""

    ATTACK_PROBABILITY = auto()
    SEED = auto()


class BB84EveQubitLabels(StrEnum):
    """Names of the qbit added by Eve in the BB84 key distribution protocol"""

    EVE_COPY = auto()
    EVE_BASE_CHOICE = auto()
    EVE_ATTACK_CHOICE = auto()


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


class TomamichelEtAlEveParams(StrEnum):
    """Parameters of Eve when attacking the Tomamichel et al. QKD protocol"""

    ATTACK_PROBABILITY = auto()
    SEED = auto()
    BLOC_SIZE = auto()
    DETECTION_SIZE = auto()


class TomamichelEtAlEveQubitLabels(StrEnum):
    """Names of the qbit added by Eve in the Tomamichel et al. QKD protocol"""

    EVE_COPY = auto()
    EVE_BASE_CHOICE = auto()
    EVE_ATTACK_CHOICE = auto()
