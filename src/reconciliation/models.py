"""Modules containing the implementation of the interfaces in interfaces.py"""

from typing import Tuple, Set, List, Dict
from math import ceil

# import copy

import numpy as np
import galois

from src.reconciliation.interfaces import ReconciliationProtocol
from src.reconciliation.schema import CascadeParams

from src.hashing import convert_string_to_gf2, get_random_toeplitz_matrix


# Needs a proof that this is directly correlated with the amount of
# information ANY Eve could get, not just the few implementation proposed in
# this project.
def find_nb_bits_revealed(
    revealed: list[tuple[int, ...]],
    key_length: int,
) -> int:
    """Computes the number of bits revealed from the shared parities

    :param revealed: The list of all parities shared
    :type revealed: list[tuple[int,...]]
    :param key_length: The length of the key that was corrected
    :type key_length: int
    :return: The number of bits revealed. Will always be <= min(len
        (revealed), key_length)
    :rtype: int
    """

    if len(revealed) == 0:
        return 0

    # FUTURE OPTIMISATION : The removal could be done faster using stuff
    # already compiled in C

    known = set()
    updated = True
    while updated:
        updated = False
        length = len(revealed)
        i = 0
        while i < length:
            if len(revealed[i]) == 1:
                known.add(int(revealed[i][0]))
                updated = True
                revealed.pop(i)
                length -= 1
            else:
                new = []
                for x in revealed[i]:
                    x = int(x)
                    if x not in known:
                        new.append(x)
                revealed[i] = np.array(new, dtype=int)
                i += 1

    matrix = np.zeros(shape=(len(revealed), key_length), dtype=np.int8)

    rows = np.repeat(np.arange(len(revealed)), [len(t) for t in revealed])
    cols = np.concatenate(revealed, dtype=int)

    matrix[rows, cols] = 1

    gf = galois.GF(2)

    return np.linalg.matrix_rank(gf(matrix)) + len(known)


class CascadeProtocol(ReconciliationProtocol):
    """Implementation of a variant of Cascade proposed by Yan et al."""

    seed: int
    number_of_passes: int
    alpha: float
    beta: float
    idx_pass_force_size: int

    def __init__(
        self,
        seed: int,
        number_of_passes: int,
        alpha: float,
        beta: float,
        idx_pass_force_size,
    ):
        super().__init__()
        self.seed = seed
        self.number_of_passes = number_of_passes
        self.alpha = alpha
        self.beta = beta
        self.idx_pass_force_size = idx_pass_force_size

    @classmethod
    def get_name(cls):
        return "cascade"

    def get_all_param_and_values(self):
        return [
            (CascadeParams.SEED, self.seed),
            (CascadeParams.NUMBER_OF_PASSES, self.number_of_passes),
            (CascadeParams.ALPHA, self.alpha),
            (CascadeParams.BETA, self.beta),
            (CascadeParams.IDX_PASS_FORCE_SIZE, self.idx_pass_force_size),
        ]

    @classmethod
    def get_instance_from_params(cls, params):
        return CascadeProtocol(
            int(params[CascadeParams.SEED]),
            int(params[CascadeParams.NUMBER_OF_PASSES]),
            float(params[CascadeParams.ALPHA]),
            float(params[CascadeParams.BETA]),
            int(params[CascadeParams.IDX_PASS_FORCE_SIZE]),
        )

    @classmethod
    def binary(
        cls,
        alice_key: List[int],
        bob_key: List[int],
        subsets: Set[Tuple[int]],
        indices: Tuple[int],
    ) -> int:
        """Corrects error if there's an odd amount of errors between Alice's
        and Bob's key in the chosen subset. NOTE : Bob's key and subsets will
        be directly modified with high likely hood.

        :param alice_key: Alice's key before doing binary -- will be "read
            only"
        :type alice_key: List[int]
        :param bob_key: Bob's key before doing binary -- can be modified
        :type bob_key: List[int]
        :param subsets: The subsets created while doing a certain pass of the
            Cascade protocol
        :type subsets: Set[Tuple[int]]
        :param indices: The indices of the current subset
        :type indices: Tuple[int]
        :return: The modified index (or -1 if no bit where changed)
        :rtype: Tuple[int,int]"""

        alice_parity = sum(alice_key[i] for i in indices) % 2
        bob_parity = sum(bob_key[i] for i in indices) % 2

        if alice_parity == bob_parity:
            return -1

        if len(indices) == 1:
            bob_key[indices[0]] = 1 - bob_key[indices[0]]
            return indices[0]

        # New subsets
        left_indices = indices[0 : len(indices) // 2]
        right_indices = indices[len(indices) // 2 : len(indices)]

        # Change the subsets
        subsets.remove(indices)
        subsets.add(left_indices)
        subsets.add(right_indices)

        left_modif = cls.binary(alice_key, bob_key, subsets, left_indices)

        if left_modif >= 0:
            return left_modif

        right_modifs = cls.binary(alice_key, bob_key, subsets, right_indices)

        return right_modifs

    @classmethod
    def do_cascade_first_pass(
        cls,
        alice_array: List[int],
        bob_array: List[int],
        all_subsets: Dict[int, Set[Tuple[int]]],
        subset_size: int,
    ) -> None:
        """
        Executes the first pass of the Cascade protocol. NOTE : bob_array and
        all_subsets will be modified
        :param alice_array: Alice's key -- Will be read only
        :type alice_array: List[int]
        :param bob_array: Bob's key
        :type bob_array: List[int]
        :param all_subsets: All the subsets separated by pass
        :type all_subsets: Dict[int,Set[Tuple[int]]]
        """
        all_subsets[1] = set()
        for subset_idx in range(ceil(len(alice_array) / subset_size)):
            curr_subset = [
                subset_idx * subset_size + bit_idx
                for bit_idx in range(
                    min(
                        subset_size,
                        len(alice_array) - subset_idx * subset_size,
                    )
                )
            ]
            curr_subset = tuple(curr_subset)
            all_subsets[1].add(curr_subset)
            cls.binary(
                alice_array,
                bob_array,
                all_subsets[1],
                curr_subset,
            )

    @classmethod
    def find_affected(
        cls,
        max_pass: int,
        all_subsets: Dict[int, Set[Tuple[int]]],
        modif_idx: int,
    ) -> Set[Tuple[int, Tuple[int]]]:
        """
        Finds all sets that contain the modified index.

        :param max_pass: The highest pass to check for
        :type max_pass: int
        :param all_subsets: All the subsets separated by pass
        :type all_subsets: Dict[int,Set[Tuple[int]]]
        :param modif_idx: The index of the modified bit
        :type modif_idx: int
        :return: The set of all the affected subset with the pass there're on
        :rtype: Set[Tuple[int,Tuple[int]]]
        """
        affected: Set[Tuple[int, Tuple[int]]] = set()
        for prev in range(1, max_pass + 1):
            for subset in all_subsets[prev]:
                # Removes all set of size 1 because they cannot have errors
                # by default
                if modif_idx in subset and len(subset) > 1:
                    affected.add((prev, subset))

        return affected

    @classmethod
    def correction_cascade(
        cls,
        alice_array: List[int],
        bob_array: List[int],
        all_subsets: Dict[int, Set[Tuple[int]]],
        curr_pass: int,
        modif_idx: int,
    ) -> None:
        """
        Corrects all new error that appeared in previous correction. NOTE :
        bob_array and all_subsets will be modified with high likely hood.

        :param alice_array: Alice's key -- Will be read only
        :type alice_array: List[int]
        :param bob_array: Bob's key
        :type bob_array: List[int]
        :param all_subsets: All the subsets separated by pass
        :type all_subsets: Dict[int,Set[Tuple[int]]]
        :param curr_pass: The index of the current pass / pass in Cascade
        :type curr_pass: int
        :param modif_idx: The index of the bit that was modified
        :type modif_idx: int
        """

        # Find all the subset affected
        # They will only be in previous passes at this point
        affected = cls.find_affected(curr_pass - 1, all_subsets, modif_idx)

        # The affected subsets are GUARANTEED to contain an odd number of errors
        while len(affected) > 0:
            # Finds the smallest affected subset and corrects it
            smallest = min(affected, key=lambda x: len(x[1]))
            affected.remove(smallest)
            new_modif_idx = cls.binary(
                alice_array,
                bob_array,
                all_subsets[smallest[0]],
                smallest[1],
            )

            # Using symmetric difference, keeps only the subsets that were
            # only affected once
            affected = affected ^ cls.find_affected(
                curr_pass, all_subsets, new_modif_idx
            )

    @classmethod
    def do_cascade_ith_pass(
        cls,
        alice_array: List[int],
        bob_array: List[int],
        all_subsets: Dict[int, Set[Tuple[int]]],
        curr_pass: int,
        subset_size: int,
        rng: np.random.Generator,
    ) -> None:
        """
        Executes the ith pass of the Cascade protocol. NOTE : bob_array and
        all_subsets will be modified

        :param alice_array: Alice's key -- Will be read only
        :type alice_array: List[int]
        :param bob_array: Bob's key
        :type bob_array: List[int]
        :param all_subsets: All the subsets separated by pass
        :type all_subsets: Dict[int,Set[Tuple[int]]]
        :param curr_pass: The pass that needs to be executed
        :type curr_pass: int
        :param subset_size: The size of the subsets created in the current
            pass
        :param rng: The random number generator that needs to be used
        :type rng: np.random.Generator
        """
        all_subsets[curr_pass] = set()
        min_val = 1
        max_val = ceil(len(alice_array) / subset_size)
        attributions = rng.integers(
            min_val,
            max_val + 1,
            size=len(alice_array),
        )

        for j in range(min_val, max_val + 1):
            curr_subset = np.where(attributions == j)[0]
            curr_subset = tuple(rng.permutation(curr_subset))
            all_subsets[curr_pass].add(curr_subset)

            modif_idx = cls.binary(
                alice_array,
                bob_array,
                all_subsets[curr_pass],
                curr_subset,
            )

            if modif_idx != -1:
                cls.correction_cascade(
                    alice_array,
                    bob_array,
                    all_subsets,
                    curr_pass,
                    modif_idx,
                )

    # TODO - optimise
    def reconciliate_keys(
        self,
        alice_raw_key,
        bob_raw_key,
        error_rate,
        correctness,
    ):
        rng = np.random.default_rng(seed=self.seed)

        alice_key, bob_key, nb_revealed, log = self.__inner_reconciliate_keys(
            rng, alice_raw_key, bob_raw_key, error_rate
        )

        same_hash, matrix, hash_a = self.verify_hash(
            rng, alice_key, bob_key, correctness
        )

        if not same_hash:
            return "", "", 0, []

        return alice_key, bob_raw_key, nb_revealed, (log, matrix, hash_a)

    def __inner_reconciliate_keys(
        self,
        rng: np.random.Generator,
        alice_raw_key: str,
        bob_raw_key: str,
        error_rate: float,
    ) -> Tuple[str, str, int, List[Tuple[int, ...]]]:
        if error_rate == 0:
            return alice_raw_key, bob_raw_key, 0, []

        alice_array = [int(a) for a in alice_raw_key]
        bob_array = [int(b) for b in bob_raw_key]

        all_subsets: Dict[int, Set[Tuple[int]]] = {}

        max_subset_size = ceil(len(alice_array) / 2)

        subset_size = min(ceil(self.alpha / error_rate), max_subset_size)

        self.do_cascade_first_pass(
            alice_array,
            bob_array,
            all_subsets,
            subset_size,
        )

        for i in range(2, self.number_of_passes + 1):
            if i < self.idx_pass_force_size:
                subset_size = min(
                    ceil(self.beta * subset_size), max_subset_size
                )
            else:
                subset_size = max_subset_size

            self.do_cascade_ith_pass(
                alice_array,
                bob_array,
                all_subsets,
                i,
                subset_size,
                rng,
            )

        revealed = []
        for list_of_subsets in all_subsets.values():
            for subset in list_of_subsets:
                revealed.append(subset)

        return (
            alice_raw_key,
            "".join(str(b) for b in bob_array),
            # find_nb_bits_revealed(
            # copy.deepcopy(revealed), len(alice_raw_key)
            # )
            len(revealed),
            revealed,
        )

    def verify_hash(
        self,
        rng: np.random.Generator,
        alice_key: str,
        bob_key: str,
        correctness: float,
    ) -> Tuple[bool, galois.FieldArray, galois.FieldArray]:
        matrix = get_random_toeplitz_matrix(
            rng,
            int(np.ceil(np.log2(1 / correctness))),
            len(alice_key),
        )

        hash_a = matrix @ convert_string_to_gf2(alice_key)

        if np.any(hash_a != matrix @ convert_string_to_gf2(bob_key)):
            return False, None, None

        return True, matrix, hash_a
