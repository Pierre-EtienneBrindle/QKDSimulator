"""Module containing all the interfaces to create custom QKD"""

from typing import List, Any, Tuple
from abc import ABC, abstractmethod

from src.distribution.core import System


class Environment(ABC):
    """Abstract class/interface that represents the generic behavior of a
    noisy environment"""

    @abstractmethod
    def get_name(self) -> str:
        """
        Gives the name of the environment

        :return: The name of the environment
        :rtype: str"""
        raise NotImplementedError("This abstract method wasn't implemented")

    @abstractmethod
    def get_all_param_and_values(self) -> List[Tuple[str, Any]]:
        """
        Gets all the parameters and returns their names and values

        :return: All names and values of each parameters as a list of tuples
        :rtype: List[Tuple[str,Any]]"""
        raise NotImplementedError("This abstract method wasn't implemented")

    @abstractmethod
    def compute_eve_bits_from_measurements(
        self,
        measurements: List[str],
        labels: List[str],
    ) -> List[str]:
        """
        For environment that represents an eavesdropper's behavior, computes
        the bits measured by Eve on each attempt. Might be used to compute
        the amount of shared entropy between Eve and Alice's raw key. If the
        environment doesn't represent an eavesdropper's behavior, the output
        will always be None.

        :return: The list of each bit measured by Eve
        :rtype: List[str]"""
        raise NotImplementedError("This abstract method wasn't implemented")

    @abstractmethod
    def apply_environment_after_segment(
        self,
        segment_number: int,
        curr_system: System,
        transmitted_qbits: List[str],
    ) -> System:
        """
        Applies the environment to the system. This operation should only
        affect qbits created for this specific environment and the qbits
        transmitted in the quantum communication channel. In the case of an
        eave's dropper, it can also read any classical communication qbit

        :param segment_number: The segment of the protocol after witch the
        environment is placed (used for Eve's)
        :type segment_number: int
        :param curr_system: The system to apply the environment to
        :type curr_system: System
        :param transmitted_qbits: The labels of the qbits that are
        transmitted over the quantum communication channel
        :type transmitted_qbits: List[str]
        :return: The system after the environment was applied. This system
        might have greater dimensions than the original one.
        :rtype: System"""
        raise NotImplementedError("This abstract method wasn't implemented")


class DistributionProtocol(ABC):
    """Abstract class/interface of all QKD protocol"""

    @abstractmethod
    def get_name(self) -> str:
        """
        Gives the name of the protocol

        :return: The name of the protocol
        :rtype: str"""
        raise NotImplementedError("This abstract method wasn't implemented")

    @abstractmethod
    def get_all_params_names_and_values(self) -> List[Tuple[str, Any]]:
        """
        Gets all the parameters and returns their names and values

        :return: All names and values of each parameters as a list of tuples
        :rtype: List[Tuple[str,Any]]"""
        raise NotImplementedError("This abstract method wasn't implemented")

    @abstractmethod
    def compute_raw_keys(
        self,
        measurements: List[str],
        labels: List[str],
    ) -> Tuple[str, str, float]:
        """
        Computes the raw key that Alice and Bob would have had after doing
        each measurement.

        :param measurements: The list of all the results of the measurements
        of the system
        :type measurements: List[str]
        :param labels: The name of each qbit to be able to identify Alice's
        and Bob's qbits
        :type labels: List[str]
        :return: Alice's raw key, Bob's raw key and the error rate in this order
        :rtype: Tuple[str,str,float]
        """
        raise NotImplementedError("This abstract method wasn't implemented")

    @abstractmethod
    def apply_protocol_segment(
        self,
        segment_number: int,
        curr_system: System,
    ) -> Tuple[System, List[str]]:
        """
        Applies a segment of the protocol to the system. A segment always end
        when Alice and/or Bob sends qbit over the quantum channel and/or
        communicate with one another.

        :param segment_number: Part of the protocol to do. Starts with 0
        :type segment_number: int
        :param curr_system: The system before the application of the protocol
        :type curr_system: System
        :return: The new system after doing the segment of the protocol and
        the labels of the qbits that will be transmitted over the quantum
        channel at the end of the segment
        :rtype: Tuple[System, List[str]]
        """
        raise NotImplementedError("This abstract method wasn't implemented")

    @abstractmethod
    def get_num_segments(self) -> int:
        """
        Gives the number of segments of the protocol

        :return: The number of segments of the protocol
        :rtype: int"""
        raise NotImplementedError("This abstract method wasn't implemented")

    # TO THINK ABOUT : ADD A COMPUTATION TRACE HAS THE OUTPUT TO AVOID
    # REDOING WORK ?
    @abstractmethod
    def is_done(self, measurements: List[str], labels: List[str]) -> bool:
        """
        Checks whether the protocol was completed or not (ie. where enough
        iterations done)

        :param measurements: The measurements that were already done.
        :type measurements: List[str]
        :param labels: The name of each bit
        :type labels: List[str]
        :return: True iff the protocol is done
        :rtype: bool"""
        raise NotImplementedError("This abstract method wasn't implemented")
