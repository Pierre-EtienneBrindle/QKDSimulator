"""Interfaces to maintain clean records"""

from typing import Any, Dict, Tuple, List
from abc import ABC, abstractmethod


class Recordable(ABC):
    """Interfaces for class that can be saved"""

    @classmethod
    @abstractmethod
    def get_instance_from_params(cls, params: Dict[str, Any]) -> Recordable:
        """
        Static constructor for the object

        :param params: The parameters of the object
        :type params: Dict[str,Any]
        :return: An instance of the class
        :rtype: Recordable
        """
        raise NotImplementedError(
            "This abstract class method wasn't implemented"
        )

    @classmethod
    @abstractmethod
    def get_name(cls) -> str:
        """
        Gives the name of the object

        :return: The name of the object
        :rtype: str"""
        raise NotImplementedError(
            "This abstract class method wasn't implemented"
        )

    @abstractmethod
    def get_all_param_and_values(self) -> List[Tuple[str, Any]]:
        """
        Gets all the parameters and returns their names and values

        :return: All names and values of each parameters as a list of tuples
        :rtype: List[Tuple[str,Any]]"""
        raise NotImplementedError("This abstract method wasn't implemented")
