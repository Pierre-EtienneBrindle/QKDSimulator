"""Implementations of different amplification"""

import numpy as np
import galois

from src.amplification.interfaces import AmplificationProtocol
from src.amplification.schema import Universal2ExtractorParams


class Universal2ExtractorProtocol(AmplificationProtocol):
    """A privacy amplification using a 2 universal extractor"""

    seed: int

    def __init__(self, seed: int):
        super().__init__()
        self.seed = seed

    def get_all_param_and_values(self):
        return [(Universal2ExtractorParams.SEED, self.seed)]

    @classmethod
    def get_instance_from_params(cls, params):
        return Universal2ExtractorProtocol(
            int(params[Universal2ExtractorParams.SEED])
        )

    @classmethod
    def get_name(cls):
        return "2-universal_extractor"

    def amplify_keys(self, alice_raw_key, bob_raw_key, max_key_length):
        rng = np.random.default_rng(seed=self.seed)

        n = len(alice_raw_key)
        m = min(n, max_key_length)

        raise NotImplementedError("THIS IS NOT IMPLEMENTED")
