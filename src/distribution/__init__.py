"""Package containing classes to help with creating custom distribution
protocols"""

from .core import System
from .interfaces import DistributionProtocol, Environment
from .models import (
    NoiselessEnvironment,
    SingleQbitDepolarization,
    SingleQbitAmplitudeDamping,
    BB84KeyDistribution,
    TomamichelEtAlKeyDistribution,
    BB84Eve,
    TomamichelEtAlEve,
)
from .schema import (
    GenDistParams,
    DepolarizingParams,
    AmplitudeDampingParams,
    BB84EveParams,
    BB84QbitLabels,
    BB84EveQubitLabels,
    BB84Params,
    TomamichelEtAlParams,
    TomamichelEtAlQbitLabels,
    TomamichelEtAlEveParams,
    TomamichelEtAlEveQubitLabels,
)
from .utils import binary_entropy

__all__ = [
    "DistributionProtocol",
    "Environment",
    "System",
    "NoiselessEnvironment",
    "SingleQbitDepolarization",
    "SingleQbitAmplitudeDamping",
    "BB84KeyDistribution",
    "TomamichelEtAlKeyDistribution",
    "BB84Eve",
    "DepolarizingParams",
    "AmplitudeDampingParams",
    "BB84EveParams",
    "BB84QbitLabels",
    "BB84EveQubitLabels",
    "BB84Params",
    "TomamichelEtAlParams",
    "TomamichelEtAlQbitLabels",
    "TomamichelEtAlEveParams",
    "TomamichelEtAlEveQubitLabels",
    "TomamichelEtAlEve",
    "binary_entropy",
    "GenDistParams",
]
