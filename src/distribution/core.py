"""Module containing the core classes for the distribution step of the QKD
protocols"""

from typing import List

from qiskit.quantum_info import DensityMatrix, Kraus


class System:
    """Class representing the system evolving during the QKD protocol

    Attributes :\n
    state (DensityMatrix) : The actual state represented as a density
                            matrix\n
    labels (List[str]) : The name of each qubit for identifying purposes
    """

    # DensityMatrix([1]) is equivalent to a zero qubit system
    state: DensityMatrix = DensityMatrix([1])

    labels: List[str] = []

    def add_qubits(self, new_labels: List[str]) -> None:
        """Adds qubits in the |0><0| state to the system

        :param new_labels: The name of the new qubits
        :type new_labels: List[str]
        """

        if len(new_labels) == 0:
            return

        new_part = DensityMatrix.from_label("0" * len(new_labels))

        self.state = self.state.expand(new_part)
        self.labels = self.labels + new_labels

    def evolve(self, channel: Kraus, quargs: List[str]) -> None:
        """Applies the evolution to the system

        :param channel: The channel to apply on the system
        :type channel: Kraus
        :param quargs: The name of the qubits to apply the channel to.
        :type quargs: List[str]
        """
        quargs_in_index = [self.labels.index(label) for label in quargs]
        self.state = self.state.evolve(channel, quargs_in_index)
