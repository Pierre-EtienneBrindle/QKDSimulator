"""Tests for all the src.distribution.core classes"""

import pytest
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator, Kraus, DensityMatrix
from src.distribution import System


@pytest.mark.parametrize(
    "labels",
    [
        ["One"],
        ["1", "2"],
        ["A", "B", "C"],
    ],
)
def test_adding_qubits_labels(labels: list[str]) -> None:
    test_system = System()
    test_system.add_qubits(labels)

    assert test_system.labels == labels


@pytest.mark.parametrize(
    "labels1,labels2",
    [
        (["1"], ["2"]),
        (["1"], []),
        ([], ["1"]),
        (["1", "2"], ["3,4"]),
    ],
)
def test_adding_qubits_correct_size(
    labels1: list[str],
    labels2: list[str],
) -> None:
    test_system = System()
    test_system.add_qubits(labels1)
    test_system.add_qubits(labels2)

    assert test_system.state.num_qubits == len(labels1) + len(labels2)


def test_evoliton() -> None:
    test_system = System()
    test_system.add_qubits(["1", "2"])

    qc = QuantumCircuit(2)

    qc.h(0)
    qc.cx(0, 1)

    op = Operator(qc)
    kraus = Kraus(op)

    test_system.evolve(kraus, ["1", "2"])

    expected_state = DensityMatrix.from_label("00")
    expected_state = expected_state.evolve(kraus, qargs=[0, 1])

    assert np.allclose(test_system.state.data, expected_state.data)
