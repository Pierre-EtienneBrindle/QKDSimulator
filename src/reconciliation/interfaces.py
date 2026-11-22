"""Modules containing all of the interfaces for a custom information
reconciliation protocol"""

from typing import Tuple, List
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
    ) -> Tuple[str, str, List[Tuple[int, ...]]]:
        """
        Tries and remove errors between Alice's and Bob's raw key

        :param alice_raw_key: Alice's raw key
        :type alice_raw_key: str
        :param bob_raw_key: Bob's raw key
        :type bob_raw_key: str
        :param error_rate: The expected error rate of the protocol
        :type error_rate: float
        :return: Alice's and Bob's key after error reconciliation. If Alice
            (resp. Bob) aborted, Alice's raw key (resp. Bob) will be the empty
            string. Also output known parities as list of indices.
        :rtype: Tuple[str,str, List[Tuple[int,...]]]
        """
        raise NotImplementedError("This abstract method wasn't implemented")
