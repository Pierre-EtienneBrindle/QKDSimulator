"""Modules containing all of the interfaces for a custom information
reconciliation protocol"""

from typing import List, Any, Tuple
from abc import ABC, abstractmethod


class ReconciliationProtocol(ABC):
    """Abstract class/interface for all information reconciliation
    protocols"""

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

    # TO THINK ABOUT : OUTPUT AMOUNT OF BIT REVEALED / AMOUNT OF ENTROPY
    # REVEALED ?
    @abstractmethod
    def reconciliate_keys(
        self,
        alice_raw_key: str,
        bob_raw_key: str,
        error_rate: float,
    ) -> Tuple[str, str]:
        """
        Tries and remove errors between Alice's and Bob's raw key

        :param alice_raw_key: Alice's raw key
        :type alice_raw_key: str
        :param bob_raw_key: Bob's raw key
        :type bob_raw_key: str
        :param error_rate: The expected error rate of the protocol
        :type error_rate: float
        :return: Alice's and Bob's key after error reconciliation
        :rtype: Tuple[str,str]
        """
        raise NotImplementedError("This abstract method wasn't implemented")
