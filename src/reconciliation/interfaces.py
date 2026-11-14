"""Modules containing all of the interfaces for a custom information
reconciliation protocol"""

from typing import Tuple
from abc import abstractmethod

from src.record_management import Recordable


class ReconciliationProtocol(Recordable):
    """Abstract class/interface for all information reconciliation
    protocols"""

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
