"""Modules giving access to different interfaces that help define a custom
privacy amplification protocol"""

from typing import Tuple
from abc import abstractmethod
from src.record_management import Recordable


class AmplificationProtocol(Recordable):
    """Abstract class/interface for all privacy amplification
    protocols"""

    @abstractmethod
    def amplify_keys(
        self,
        alice_raw_key: str,
        bob_raw_key: str,
        max_key_length: int,
    ) -> Tuple[str, str]:
        """
        Tries to minimise the shared information of an eavesdropper and Alice's key

        :param alice_raw_key: Alice's raw key
        :type alice_raw_key: str
        :param bob_raw_key: Bob's raw key
        :type bob_raw_key: str
        :param max_key_length: The maximal secure key length that the
            protocol can produce
        :type max_key_length: int
        :return: Alice's and Bob's key after privacy amplification. If Alice
            (resp. Bob) aborted, Alice's raw key (resp. Bob) will be the empty
            string ("").
        :rtype: Tuple[str,str]
        """
        raise NotImplementedError("This abstract method wasn't implemented")
