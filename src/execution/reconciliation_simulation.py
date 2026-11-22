"""Module that gives access to function to simulate a given information
reconciliation protocol"""

import numpy as np
import galois

from src.reconciliation import ReconciliationProtocol
from src.data_management import DataBase, RunCols
from src.execution.utils import base_2_to_base_16, base_16_to_base_2


def find_nb_bits_revealed(
    revealed: list[tuple[int, ...]],
    key_length: int,
) -> int:
    """Computes the number of bits revealed from the shared parities

    :param revealed: The list of all parities shared
    :type revealed: list[tuple[int,...]]
    :param key_length: The length of the key that was corrected
    :type key_length: int
    :return: The number of bits revealed
    :rtype: int
    """

    matrix = np.zeros(shape=(len(revealed), key_length), dtype=np.int8)

    rows = np.repeat(np.arange(len(revealed)), [len(t) for t in revealed])
    cols = np.concatenate(revealed)

    matrix[rows, cols] = 1

    gf = galois.GF(2)

    return np.linalg.matrix_rank(gf(matrix))


def execute_reconciliation_and_store(
    db: DataBase, reconciliation_protocol: ReconciliationProtocol, run_id: int
) -> int:
    """Executes the information reconciliation protocol and store the result
    of the execution inside the data base.

    :param db: The database to save the result of the information
    reconciliation attempt into
    :type db: DataBase
    :param reconciliation_protocol: The protocol to execute
    :type reconciliation_protocol: ReconciliationProtocol
    :param run_id: The id of the run that produced the keys
    :type run_id: int
    :return: The id of the reconciliation attempt or -1 if the reconciliation
        couldn't be attempted
    :rtype: int"""

    run_info = db.run[db.run[RunCols.ID] == run_id]
    alice_raw: str = run_info[RunCols.ALICE_KEY].iloc[0]
    bob_raw: str = run_info[RunCols.BOB_KEY].iloc[0]
    error_rate: float = run_info[RunCols.ERROR_RATE].iloc[0]

    if alice_raw == "" or bob_raw == "":
        return -1

    alice_key, bob_key, revealed = reconciliation_protocol.reconciliate_keys(
        base_16_to_base_2(alice_raw),
        base_16_to_base_2(bob_raw),
        error_rate,
    )

    reconciliation_id = db.load_reconciliation(
        reconciliation_protocol.get_name(),
        run_id,
        base_2_to_base_16(alice_key),
        base_2_to_base_16(bob_key),
        find_nb_bits_revealed(revealed, len(alice_key)),
    )

    db.load_reconciliation_params(
        reconciliation_id,
        reconciliation_protocol.get_all_param_and_values(),
    )

    return reconciliation_id
