"""Package giving access to interfaces and data classes that can be used to
create custom privacy amplification protocols"""

from .interfaces import AmplificationProtocol
from .schema import Universal2ExtractorParams
from .models import Universal2ExtractorProtocol

__all__ = [
    "AmplificationProtocol",
    "Universal2ExtractorParams",
    "Universal2ExtractorProtocol",
]
