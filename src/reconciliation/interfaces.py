"""Modules containing all of the interfaces for a custom information
reconciliation protocol"""

from typing import Tuple, Any
from abc import abstractmethod

from src.record_management import Recordable


class ReconciliationProtocol(Recordable):
    """Abstract class/interface for all information reconciliation
    protocols"""

    @abstractmethod
    def reconciliate_keys(
        self,
        alice_raw_key: str,
        bob_raw_key: str,
        error_rate: float,
        correctness: float,
    ) -> Tuple[str, str, int, Any]:
        """
        Tries and remove errors between Alice's and Bob's raw key

        :param alice_raw_key: Alice's raw key
        :type alice_raw_key: str
        :param bob_raw_key: Bob's raw key
        :type bob_raw_key: str
        :param error_rate: The expected error rate of the protocol
        :type error_rate: float
        :param correctness: The probability that both key are identical at
            the end.
        :type correctness: float
        :return: Alice's and Bob's key after error reconciliation. If Alice
            (resp. Bob) aborted, Alice's raw key (resp. Bob) will be the empty
            string. Also output the number of bits shared and any data Eve could have collected
        :rtype: Tuple[str,str, int, Any]
        """
        raise NotImplementedError("This abstract method wasn't implemented")
