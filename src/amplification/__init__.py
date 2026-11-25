"""Package giving access to interfaces and data classes that can be used to
create custom privacy amplification protocols"""

from .interfaces import AmplificationProtocol
from .schema import ToeplitzAmpParams
from .models import ToeplitzAmplificationProtocol

__all__ = [
    "AmplificationProtocol",
    "ToeplitzAmpParams",
    "ToeplitzAmplificationProtocol",
]
