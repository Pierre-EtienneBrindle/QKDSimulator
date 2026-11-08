"""Modules giving access to different interfaces that help define a custom
privacy amplification protocol"""

from typing import List, Any, Tuple
from abc import ABC, abstractmethod


class AmplificationProtocol(ABC):
    """Abstract class/interface for all privacy amplification
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

    # TO THINK ABOUT : GET ERROR RATE AND AMOUNT OF BIT REVEALED ? - Could be
    # though params when constructing the object
    @abstractmethod
    def amplify_keys(
        self, alice_raw_key: str, bob_raw_key: str
    ) -> Tuple[str, str]:
        """
        Tries to minimise the shared information of an eavesdropper and Alice's key

        :param alice_raw_key: Alice's raw key
        :type alice_raw_key: str
        :param bob_raw_key: Bob's raw key
        :type bob_raw_key: str
        :return: Alice's and Bob's key after privacy amplification
        :rtype: Tuple[str,str]
        """
        raise NotImplementedError("This abstract method wasn't implemented")
