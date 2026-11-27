"""Implementations of different amplification"""

import numpy as np

from src.amplification.interfaces import AmplificationProtocol
from src.amplification.schema import ToeplitzAmpParams

from src.hashing import get_random_toeplitz_matrix, convert_string_to_gf2


class ToeplitzAmplificationProtocol(AmplificationProtocol):
    """A privacy amplification using Toeplitz matrix"""

    seed: int

    def __init__(self, seed: int):
        super().__init__()
        self.seed = seed

    def get_all_param_and_values(self):
        return [(ToeplitzAmpParams.SEED, self.seed)]

    @classmethod
    def get_instance_from_params(cls, params):
        return ToeplitzAmplificationProtocol(
            int(params[ToeplitzAmpParams.SEED])
        )

    @classmethod
    def get_name(cls):
        return "toeplitz-matrix"

    def amplify_keys(self, alice_raw_key, bob_raw_key, max_key_length):

        if max_key_length <= 0:
            return "", ""

        rng = np.random.default_rng(seed=self.seed)

        n = len(alice_raw_key)

        matrix = get_random_toeplitz_matrix(rng, min(n, max_key_length), n)

        alice = matrix @ convert_string_to_gf2(alice_raw_key)
        bob = matrix @ convert_string_to_gf2(bob_raw_key)

        return "".join(str(a) for a in alice), "".join(str(b) for b in bob)
