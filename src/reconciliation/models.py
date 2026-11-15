"""Modules containing the implementation of the interfaces in interfaces.py"""

from typing import Tuple, Set, List, Dict
from math import ceil

import numpy as np

from src.reconciliation.interfaces import ReconciliationProtocol
from src.reconciliation.schema import CascadeParams


class CascadeProtocol(ReconciliationProtocol):
    """Implementation of a variant of Cascade proposed by Yan et al."""

    seed: int
    number_of_passes: int

    def __init__(
        self,
        seed: int,
        number_of_passes: int,
    ):
        super().__init__()
        self.seed = seed
        self.number_of_passes = number_of_passes

    @classmethod
    def get_name(cls):
        return "cascade"

    def get_all_param_and_values(self):
        return [
            (CascadeParams.SEED, self.seed),
            (CascadeParams.NUMBER_OF_PASSES, self.number_of_passes),
        ]

    @classmethod
    def get_instance_from_params(cls, params):
        return CascadeProtocol(
            int(params[CascadeParams.SEED]),
            int(params[CascadeParams.NUMBER_OF_PASSES]),
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

        if left_modif > 0:
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
            # This should not happen in theory
            if new_modif_idx == -1:
                print("Error in CascadeProtocol's logic -- No side effect")
                continue

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
        :param subset_size: The size of the subsets created in the current pass
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
            curr_subset = tuple(curr_subset)
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

    def reconciliate_keys(self, alice_raw_key, bob_raw_key, error_rate):
        subset_size = ceil(
            0.8 / (error_rate + 0.0001)
        )  # Adds a small buffer to avoid division by 0

        alice_array = [int(a) for a in alice_raw_key]
        bob_array = [int(b) for b in bob_raw_key]

        rng = np.random.default_rng(seed=self.seed)
        all_subsets: Dict[int, Set[Tuple[int]]] = {}

        self.do_cascade_first_pass(
            alice_array,
            bob_array,
            all_subsets,
            subset_size,
        )

        for i in range(2, self.number_of_passes + 1):
            subset_size = min(5 * subset_size, ceil(len(alice_array) / 2))
            self.do_cascade_ith_pass(
                alice_array,
                bob_array,
                all_subsets,
                i,
                subset_size,
                rng,
            )

        return alice_raw_key, "".join(str(bob_array))
