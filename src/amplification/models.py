"""Implementations of different amplification"""

import numpy as np
import galois

from src.amplification.interfaces import AmplificationProtocol
from src.amplification.schema import ToeplitzAmpParams


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
        return "2-universal_extractor"

    def amplify_keys(self, alice_raw_key, bob_raw_key, max_key_length):
        rng = np.random.default_rng(seed=self.seed)

        n = len(alice_raw_key)
        m = min(n, max_key_length)

        values = rng.integers(0, 2, size=n + m - 1)

        matrix = np.zeros(shape=(m, n), dtype=np.uint8)

        for i in range(m):
            for j in range(n):
                matrix[i, j] = values[n - 1 + i - j]

        gf2 = galois.GF(2)

        matrix = gf2(matrix)

        alice = gf2(np.array([int(a) for a in alice_raw_key]))
        bob = gf2(np.array([int(b) for b in bob_raw_key]))

        alice = matrix @ alice
        bob = matrix @ bob

        return "".join(str(a) for a in alice), "".join(str(b) for b in bob)
