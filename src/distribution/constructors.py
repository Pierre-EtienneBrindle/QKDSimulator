"""Module containing the dictionary constructor of different distribution
classes. This will be important for the reconstruction of a protocol from the
name and values of it's parameters"""

from typing import Dict, Any

from src.distribution.models import (
    NoiselessEnvironment,
    SingleQbitDepolarization,
    SingleQuitAmplitudeDamping,
    BB84KeyDistribution,
    TomamichelEtAlKeyDistribution,
)
from src.distribution.schema import (
    DepolarizingParams,
    AmplitudeDampingParams,
    BB84Params,
    TomamichelEtAlParams,
)


def create_noiseless_environment(
    params: Dict[str, Any],
) -> NoiselessEnvironment:
    """Creates a noiseless environment (ONLY FOR FORMATTING SAKE)

    :param params: USELESS
    :type params: Dict[str,Any]
    :return: A noiseless environment
    :rtype: NoiselessEnvironment"""
    return NoiselessEnvironment()


def create_single_qbit_depolarization(
    params: Dict[str, Any],
) -> SingleQbitDepolarization:
    """Creates a single qbit depolarizing channel from the dictionary of
    parameters.

    :param params: The parameters of the depolarizing channel
    :type params: Dict[str,Any]
    :return: The single qbit depolarization channel made from the
    parameters
    :rtype: SingleQbitDepolarization"""

    return SingleQbitDepolarization(params[DepolarizingParams.PROBABILITY])


def create_single_qbit_amplitude_damping(
    params: Dict[str, Any],
) -> SingleQuitAmplitudeDamping:
    """Creates a single qbit amplitude damping channel from the dictionary of parameters

    :param params: The parameters of the amplitude damping channel
    :type params: Dict[str,Any]
    :return: The single qbit amplitude damping channel made from the
    parameters
    :rtype: SingleQbitAmplitudeDamping"""

    return SingleQuitAmplitudeDamping(
        params[AmplitudeDampingParams.PROBABILITY]
    )


def create_bb84_protocol(params: Dict[str, Any]) -> BB84KeyDistribution:
    """Creates an instance of the BB84 key distribution protocol from the
    dictionary of parameters

    :param params: The parameters of the BB84 key distribution protocol
    :type params: Dict[str,Any]
    :return: An instance of the BB84 protocol
    :rtype: BB84KeyDistribution"""

    return BB84KeyDistribution(
        params[BB84Params.MAX_ERROR_RATE],
        params[BB84Params.TARGET_KEY_SIZE],
        params[BB84Params.RANDOM_SEED],
    )


def create_tomamichel_et_al_protocol(
    params: Dict[str, Any],
) -> TomamichelEtAlKeyDistribution:
    """Creates an instance of the Tomamichel et al. key distribution protocol
    from the dictionary of parameters

    :param params: The parameters of the Tomamichel et al. key distribution protocol
    :type params: Dict[str,Any]
    :return: An instance of the Tomamichel et al. protocol
    :rtype: TomamichelEtAlKeyDistribution"""

    return TomamichelEtAlKeyDistribution(
        params[TomamichelEtAlParams.BLOC_SIZE],
        params[TomamichelEtAlParams.DETECTION_SIZE],
        params[TomamichelEtAlParams.MAX_ERROR_RATE],
        params[TomamichelEtAlParams.RANDOM_SEED],
    )
