"""Instances of the different interfaces"""

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Kraus, Operator

from src.distribution.core import System
from src.distribution.interfaces import Environment, DistributionProtocol
from src.distribution.schema import (
    DepolarizingParams,
    AmplitudeDampingParams,
    BB84Params,
    BB84QbitLabels,
    BB84EveParams,
    BB84EveQubitLabels,
    TomamichelEtAlParams,
    TomamichelEtAlQbitLabels,
    TomamichelEtAlEveParams,
    TomamichelEtAlEveQubitLabels,
)


class NoiselessEnvironment(Environment):
    """Class for an environment that doesn't produce noise"""

    @classmethod
    def get_instance_from_params(cls, params):
        return NoiselessEnvironment()

    def apply_environment_after_segment(
        self, segment_number, curr_system, transmitted_qbits
    ):
        return curr_system

    def get_all_param_and_values(self):
        return []

    @classmethod
    def get_name(cls):
        return "noiseless_environment"

    def compute_eve_info(self, measurements, labels):
        raise NotImplementedError("This environment doesn't represent an Eve")

    @classmethod
    def is_eve(cls):
        return False


class SingleQbitDepolarization(Environment):
    """Class for an environment that applies a depolarizing noise on each
    transmitted qbit individually"""

    p: float = 0

    def __init__(self, prob: float):
        super().__init__()
        self.p = prob

    @classmethod
    def get_instance_from_params(cls, params):
        return SingleQbitDepolarization(
            params[DepolarizingParams.PROBABILITY]
        )

    @classmethod
    def get_name(cls):
        return "single_qbit_depolarization"

    def get_all_param_and_values(self):
        return [(DepolarizingParams.PROBABILITY, self.p)]

    def compute_eve_info(self, measurements, labels):
        raise NotImplementedError("This environment doesn't represent an Eve")

    def apply_environment_after_segment(
        self, segment_number, curr_system, transmitted_qbits
    ):

        e_x = np.sqrt(self.p / 4) * Operator.from_label("X").data
        e_y = np.sqrt(self.p / 4) * Operator.from_label("Y").data
        e_z = np.sqrt(self.p / 4) * Operator.from_label("Z").data
        e_i = np.sqrt(1 - 3 * self.p / 4) * Operator.from_label("I").data

        kraus = Kraus([e_x, e_y, e_z, e_i])

        for qbit in transmitted_qbits:
            curr_system.evolve(kraus, [qbit])

        return curr_system

    @classmethod
    def is_eve(cls):
        return False


class SingleQbitAmplitudeDamping(Environment):
    """Class for an environment that applies an amplitude damping channel
    only to the transmitted qbits"""

    p: float = 0

    def __init__(self, prob: float):
        super().__init__()
        self.p = prob

    @classmethod
    def get_instance_from_params(cls, params):
        return SingleQbitAmplitudeDamping(
            params[AmplitudeDampingParams.PROBABILITY]
        )

    @classmethod
    def get_name(cls):
        return "single_qbit_amplitude_damping"

    def get_all_param_and_values(self):
        return [(AmplitudeDampingParams.PROBABILITY, self.p)]

    def apply_environment_after_segment(
        self, segment_number, curr_system, transmitted_qbits
    ):
        e_0 = np.array([[1.0, 0], [0.0, np.sqrt(1 - self.p)]])
        e_1 = np.array([[0.0, np.sqrt(self.p)], [0.0, 0.0]])
        kraus = Kraus([e_0, e_1])

        for qbit in transmitted_qbits:
            curr_system.evolve(kraus, [qbit])

        return curr_system

    def compute_eve_info(self, measurements, labels):
        raise NotImplementedError("This environment doesn't represent an Eve")

    @classmethod
    def is_eve(cls):
        return False


class BB84KeyDistribution(DistributionProtocol):
    """Class for the BB84 key distribution protocol"""

    max_error_rate: float = 0
    target_key_size: int = 10
    random_seed: int = 0

    def __init__(
        self,
        max_error_rate: float,
        target_key_size: int,
        random_seed: int,
    ):
        super().__init__()
        self.max_error_rate = max_error_rate
        self.target_key_size = target_key_size
        self.random_seed = random_seed

    @classmethod
    def get_instance_from_params(cls, params):
        return BB84KeyDistribution(
            params[BB84Params.MAX_ERROR_RATE],
            params[BB84Params.TARGET_KEY_SIZE],
            params[BB84Params.RANDOM_SEED],
        )

    @classmethod
    def get_name(cls):
        return "BB84_key_distribution"

    def get_all_param_and_values(self):
        return [
            (BB84Params.TARGET_KEY_SIZE, self.target_key_size),
            (BB84Params.MAX_ERROR_RATE, self.max_error_rate),
            (BB84Params.RANDOM_SEED, self.random_seed),
        ]

    def compute_raw_keys(self, measurements, labels):
        alice_bit_idx = labels.index(BB84QbitLabels.ALICE_BIT_CHOICE)
        alice_base_idx = labels.index(BB84QbitLabels.ALICE_BASE_CHOICE)
        bob_base_idx = labels.index(BB84QbitLabels.BOB_BASE_CHOICE)
        bob_measurement_idx = labels.index(BB84QbitLabels.TRANSMITTED)

        base_match = [
            i
            for i, m in enumerate(measurements)
            if m[alice_base_idx] == m[bob_base_idx]
        ]
        alice_key = [
            m[alice_bit_idx]
            for i, m in enumerate(measurements)
            if i in base_match
        ]
        bob_key = [
            m[bob_measurement_idx]
            for i, m in enumerate(measurements)
            if i in base_match
        ]

        # Sets the random seed each time to make results determinist.
        # This shouldn't be done in practice, but it's needed for the
        # analysis of the protocol
        rng = np.random.default_rng(int(self.random_seed))
        random_subset = rng.integers(low=0, high=2, size=len(alice_key))
        error_rate = sum(
            alice_key[i] != bob_key[i]
            for i, is_detection in enumerate(random_subset)
            if is_detection == 1
        ) / np.sum(random_subset == 1)

        # If there's to much error, they abort
        if error_rate > self.max_error_rate:
            return "", "", error_rate

        alice_key = "".join(
            bit for i, bit in enumerate(alice_key) if random_subset[i] == 0
        )
        bob_key = "".join(
            bit for i, bit in enumerate(bob_key) if random_subset[i] == 0
        )

        return alice_key, bob_key, error_rate

    def get_num_segments(self):
        return 2

    def apply_protocol_segment(self, segment_number, curr_system):
        match (segment_number):
            case 0:
                curr_system = System()
                curr_system.add_qbits(list(BB84QbitLabels))
                curr_system.evolve(
                    self.alice_state_preparation_channel(),
                    [
                        BB84QbitLabels.ALICE_BIT_CHOICE,
                        BB84QbitLabels.ALICE_BASE_CHOICE,
                        BB84QbitLabels.TRANSMITTED,
                    ],
                )
                return curr_system, [BB84QbitLabels.TRANSMITTED]
            case 1:
                curr_system.evolve(
                    self.bob_state_measurement_channel(),
                    [
                        BB84QbitLabels.BOB_BASE_CHOICE,
                        BB84QbitLabels.TRANSMITTED,
                    ],
                )
                return curr_system, []
            case _:
                raise ValueError("The segment number is invalide")

    def alice_state_preparation_channel(self) -> Kraus:
        """Alice prepares a random qbit in a BB84 state"""
        qc = QuantumCircuit(3)
        qc.h(0)
        qc.h(1)
        qc.cx(0, 2)
        qc.ch(1, 2)

        return Kraus(qc)

    def bob_state_measurement_channel(self) -> Kraus:
        """Bob reads the random BB84 state in a random basis"""
        qc = QuantumCircuit(2)
        qc.h(0)
        qc.ch(0, 1)

        return Kraus(qc)

    def is_done(self, measurements, labels):
        # NOT SURE ABOUT THE CONSTANT
        return (
            len(measurements)
            >= 4 * (1 + 2 * self.max_error_rate) * self.target_key_size
        )


class BB84Eve(Environment):
    """Class representing the behavior of an eavesdropper trying to listen to
    a BB84 key distribution instance"""

    p: float
    seed: int

    def __init__(self, attack_probability: float, seed: int):
        """NOTE : seed NEEDS to be the same as BB84 protocol it's attacking"""
        super().__init__()
        self.p = attack_probability
        self.seed = seed

    @classmethod
    def get_name(cls):
        return "BB84_eve"

    @classmethod
    def get_instance_from_params(cls, params):
        return BB84Eve(
            params[BB84EveParams.ATTACK_PROBABILITY],
            params[BB84EveParams.SEED],
        )

    @classmethod
    def is_eve(cls):
        return True

    def get_all_param_and_values(self):
        return [
            (BB84EveParams.ATTACK_PROBABILITY, self.p),
            (BB84EveParams.SEED, self.seed),
        ]

    def apply_environment_after_segment(
        self, segment_number, curr_system, transmitted_qbits
    ):
        match (segment_number):
            case 0:
                curr_system.add_qbits(list(BB84EveQubitLabels))
                curr_system.evolve(
                    self.eve_state_pseudo_measurement(),
                    [
                        transmitted_qbits[0],
                        BB84EveQubitLabels.EVE_COPY,
                        BB84EveQubitLabels.EVE_BASE_CHOICE,
                        BB84EveQubitLabels.EVE_ATTACK_CHOICE,
                    ],
                )
                return curr_system
            case _:
                return curr_system

    def eve_state_pseudo_measurement(self):
        """Creates a circuit where Eve pseudo-measures the transmitted qubit"""

        # Create circuit where Eve has a 50/50 prob of pseudo-measuring in X or Z basis
        pseudo_measure_qc = QuantumCircuit(3)
        pseudo_measure_qc.h(2)
        pseudo_measure_qc.ch(2, 0)
        pseudo_measure_qc.cx(0, 1)
        pseudo_measure_qc.ch(2, 0)

        pseudo_measure_ctrl_gate = pseudo_measure_qc.to_gate().control(
            num_ctrl_qubits=1, ctrl_state="1"
        )

        qc = QuantumCircuit(4)
        angle = 2 * np.asin(np.sqrt(self.p))
        qc.ry(angle, 3)
        qc.append(pseudo_measure_ctrl_gate, range(4))

        return Kraus(qc)

    def compute_eve_info(self, measurements, labels):
        alice_base_idx = labels.index(BB84QbitLabels.ALICE_BASE_CHOICE)
        bob_base_idx = labels.index(BB84QbitLabels.BOB_BASE_CHOICE)
        eve_base_idx = labels.index(BB84EveQubitLabels.EVE_BASE_CHOICE)
        eve_attack_idx = labels.index(BB84EveQubitLabels.EVE_ATTACK_CHOICE)
        eve_bit_idx = labels.index(BB84EveQubitLabels.EVE_COPY)

        kept_measurements = [
            m for m in measurements if m[alice_base_idx] == m[bob_base_idx]
        ]

        rng = np.random.default_rng(int(self.seed))
        random_subset = rng.integers(
            low=0, high=2, size=len(kept_measurements)
        )

        kept_measurements = [
            m
            for i, m in enumerate(kept_measurements)
            if random_subset[i] == 0
        ]

        return "".join(
            (
                m[eve_bit_idx]
                if m[eve_base_idx] == m[alice_base_idx]
                and m[eve_attack_idx] == "1"
                else "x"
            )
            for m in kept_measurements
        )


class TomamichelEtAlKeyDistribution(DistributionProtocol):
    """Class for the QKD protocol introduced by Tomamichel et al."""

    bloc_size: int = 0
    detection_size: int = 0
    max_error_rate: float = 0
    random_seed: int = 0

    def __init__(
        self,
        bloc_size: int,
        detection_size: int,
        max_error_rate: float,
        random_seed: int,
    ):
        super().__init__()
        self.max_error_rate = max_error_rate
        self.bloc_size = bloc_size
        self.detection_size = detection_size
        self.random_seed = random_seed

    @classmethod
    def get_instance_from_params(cls, params):
        return TomamichelEtAlKeyDistribution(
            params[TomamichelEtAlParams.BLOC_SIZE],
            params[TomamichelEtAlParams.DETECTION_SIZE],
            params[TomamichelEtAlParams.MAX_ERROR_RATE],
            params[TomamichelEtAlParams.RANDOM_SEED],
        )

    @classmethod
    def get_name(cls):
        return "tomamichel_et_al_key_distribution"

    def get_all_param_and_values(self):
        return [
            (TomamichelEtAlParams.MAX_ERROR_RATE, self.max_error_rate),
            (TomamichelEtAlParams.BLOC_SIZE, self.bloc_size),
            (TomamichelEtAlParams.DETECTION_SIZE, self.detection_size),
            (TomamichelEtAlParams.RANDOM_SEED, self.random_seed),
        ]

    def compute_raw_keys(self, measurements, labels):
        alice_bit_idx = labels.index(
            TomamichelEtAlQbitLabels.ALICE_BIT_CHOICE
        )
        alice_base_idx = labels.index(
            TomamichelEtAlQbitLabels.ALICE_BASE_CHOICE
        )
        bob_base_idx = labels.index(TomamichelEtAlQbitLabels.BOB_BASE_CHOICE)
        bob_measurement_idx = labels.index(
            TomamichelEtAlQbitLabels.TRANSMITTED
        )

        bloc = [
            i
            for i, m in enumerate(measurements)
            if m[alice_base_idx] == m[bob_base_idx]
            and m[alice_base_idx] == "1"
        ]
        detection = [
            i
            for i, m in enumerate(measurements)
            if m[alice_base_idx] == m[bob_base_idx]
            and m[alice_base_idx] == "0"
        ]

        error_rate = sum(
            m[alice_bit_idx] != m[bob_measurement_idx]
            for i, m in enumerate(measurements)
            if i in detection
        ) / len(detection)

        if error_rate > self.max_error_rate:
            return "", "", error_rate

        # Sets the random seed each time to make results determinist.
        # This shouldn't be done in practice, but it's needed for the
        # analysis of the protocol
        rng = np.random.default_rng(int(self.random_seed))
        key_subset = rng.choice(bloc, size=int(self.bloc_size), replace=False)

        alice_key = "".join(
            m[alice_bit_idx]
            for i, m in enumerate(measurements)
            if i in key_subset
        )
        bob_key = "".join(
            m[bob_measurement_idx]
            for i, m in enumerate(measurements)
            if i in key_subset
        )

        return alice_key, bob_key, error_rate

    def get_num_segments(self):
        return 2

    def apply_protocol_segment(self, segment_number, curr_system):
        match (segment_number):
            case 0:
                curr_system = System()
                curr_system.add_qbits(list(TomamichelEtAlQbitLabels))
                curr_system.evolve(
                    self.alice_state_preparation_channel(),
                    [
                        TomamichelEtAlQbitLabels.ALICE_BIT_CHOICE,
                        TomamichelEtAlQbitLabels.ALICE_BASE_CHOICE,
                        TomamichelEtAlQbitLabels.TRANSMITTED,
                    ],
                )
                return curr_system, [TomamichelEtAlQbitLabels.TRANSMITTED]
            case 1:
                curr_system.evolve(
                    self.bob_state_measurement_channel(),
                    [
                        TomamichelEtAlQbitLabels.BOB_BASE_CHOICE,
                        TomamichelEtAlQbitLabels.TRANSMITTED,
                    ],
                )
                return curr_system, []
            case _:
                raise ValueError("The segment number is invalide")

    def compute_angle_for_base_choice(self) -> float:
        """Compute the angle to get the right probability to choose the X
        basis"""
        px = 1 / (1 + np.sqrt(self.detection_size / self.bloc_size))
        return 2 * np.asin(np.sqrt(px))

    def alice_state_preparation_channel(self) -> Kraus:
        """Alice prepares a random qbit in a BB84 state"""
        qc = QuantumCircuit(3)
        qc.h(0)
        qc.ry(self.compute_angle_for_base_choice(), 1)
        qc.cx(0, 2)
        qc.ch(1, 2)

        return Kraus(qc)

    def bob_state_measurement_channel(self) -> Kraus:
        """Bob reads the random BB84 state in a random basis"""
        qc = QuantumCircuit(2)
        qc.ry(self.compute_angle_for_base_choice(), 0)
        qc.ch(0, 1)

        return Kraus(qc)

    def is_done(self, measurements, labels):
        if measurements is None or len(measurements) == 0:
            return False

        bob_basis_idx = labels.index(TomamichelEtAlQbitLabels.BOB_BASE_CHOICE)
        alice_basis_idx = labels.index(
            TomamichelEtAlQbitLabels.ALICE_BASE_CHOICE
        )
        bloc_len = len(
            [
                i
                for i, m in enumerate(measurements)
                if m[bob_basis_idx] == m[alice_basis_idx]
                and m[bob_basis_idx] == "1"
            ]
        )
        detection_len = len(
            [
                i
                for i, m in enumerate(measurements)
                if m[bob_basis_idx] == m[alice_basis_idx]
                and m[bob_basis_idx] == "0"
            ]
        )

        return (
            bloc_len >= self.bloc_size
            and detection_len >= self.detection_size
        )


class TomamichelEtAlEve(Environment):
    """Class representing the behavior of an eavesdropper trying to listen to
    a Tomamichel et al. QKD protocol instance"""

    p: float
    seed: int
    bloc_size: int
    detection_size: int

    def __init__(
        self,
        probability: float,
        seed: int,
        bloc_size: int,
        detection_size: int,
    ):
        """NOTE : seed, bloc_size and detection_size should be the same as
        the Tomamichel et al. QKD protocol instance"""
        super().__init__()
        self.p = probability
        self.seed = seed
        self.bloc_size = bloc_size
        self.detection_size = detection_size

    @classmethod
    def get_name(cls):
        return "tomamichel_eve"

    @classmethod
    def get_instance_from_params(cls, params):
        return TomamichelEtAlEve(
            params[TomamichelEtAlEveParams.ATTACK_PROBABILITY],
            params[TomamichelEtAlEveParams.SEED],
            params[TomamichelEtAlEveParams.BLOC_SIZE],
            params[TomamichelEtAlEveParams.DETECTION_SIZE],
        )

    def get_all_param_and_values(self):
        return [
            (TomamichelEtAlEveParams.ATTACK_PROBABILITY, self.p),
            (TomamichelEtAlEveParams.SEED, self.seed),
            (TomamichelEtAlEveParams.BLOC_SIZE, self.bloc_size),
            (TomamichelEtAlEveParams.DETECTION_SIZE, self.detection_size),
        ]

    @classmethod
    def is_eve(cls):
        return True

    def apply_environment_after_segment(
        self, segment_number, curr_system, transmitted_qbits
    ):
        match (segment_number):
            case 0:
                curr_system.add_qbits(list(TomamichelEtAlEveQubitLabels))
                curr_system.evolve(
                    self.eve_state_pseudo_measurement(),
                    [
                        transmitted_qbits[0],
                        TomamichelEtAlEveQubitLabels.EVE_COPY,
                        TomamichelEtAlEveQubitLabels.EVE_BASE_CHOICE,
                        TomamichelEtAlEveQubitLabels.EVE_ATTACK_CHOICE,
                    ],
                )
                return curr_system
            case _:
                return curr_system

    def compute_angle_for_base_choice(self) -> float:
        """Compute the angle to get the right probability to choose the X
        basis"""
        px = 1 / (1 + np.sqrt(self.detection_size / self.bloc_size))
        return 2 * np.asin(np.sqrt(px))

    def eve_state_pseudo_measurement(self):
        """Creates a circuit where Eve pseudo-measures the transmitted qubit"""

        # Create circuit where
        pseudo_measure_qc = QuantumCircuit(3)
        pseudo_measure_qc.ry(self.compute_angle_for_base_choice(), 2)
        pseudo_measure_qc.ch(2, 0)
        pseudo_measure_qc.cx(0, 1)
        pseudo_measure_qc.ch(2, 0)

        pseudo_measure_ctrl_gate = pseudo_measure_qc.to_gate().control(
            num_ctrl_qubits=1, ctrl_state="1"
        )

        qc = QuantumCircuit(4)
        angle = 2 * np.asin(np.sqrt(self.p))
        qc.ry(angle, 3)
        qc.append(pseudo_measure_ctrl_gate, range(4))

        return Kraus(qc)

    def compute_eve_info(self, measurements, labels):
        alice_base_idx = labels.index(
            TomamichelEtAlQbitLabels.ALICE_BASE_CHOICE
        )
        bob_base_idx = labels.index(TomamichelEtAlQbitLabels.BOB_BASE_CHOICE)
        eve_base_idx = labels.index(
            TomamichelEtAlEveQubitLabels.EVE_BASE_CHOICE
        )
        eve_attack_idx = labels.index(
            TomamichelEtAlEveQubitLabels.EVE_ATTACK_CHOICE
        )
        eve_copy_idx = labels.index(TomamichelEtAlEveQubitLabels.EVE_COPY)

        bloc = [
            i
            for i, m in enumerate(measurements)
            if m[alice_base_idx] == m[bob_base_idx]
            and m[alice_base_idx] == "1"
        ]

        rng = np.random.default_rng(int(self.seed))
        key_subset = rng.choice(bloc, size=int(self.bloc_size), replace=False)

        return "".join(
            (
                m[eve_copy_idx]
                if m[eve_attack_idx] == "1"
                and m[eve_base_idx] == m[alice_base_idx]
                else "x"
            )
            for i, m in enumerate(measurements)
            if i in key_subset
        )
