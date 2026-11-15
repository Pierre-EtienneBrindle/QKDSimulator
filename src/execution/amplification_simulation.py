"""Module that gives access to function to simulate a given privacy
amplification protocol"""

from src.amplification import AmplificationProtocol
from src.data_management import (
    DataBase,
    RecCols,
)
from src.execution.utils import base_2_to_base_16, base_16_to_base_2


def execute_amplification_and_store(
    db: DataBase,
    amplification_protocol: AmplificationProtocol,
    reconciliation_id: int,
) -> int:
    """Executes the privacy amplification protocol and store the result of the
    execution inside the data base.

    :param db: The database to save the result of the information
    amplification attempt into
    :type db: DataBase
    :param amplification_protocol: The protocol to execute
    :type amplification_protocol: AmplificationProtocol
    :param reconciliation_id: The id of the information reconciliation
    attempt that produced the keys
    :type reconciliation_id: int
    :return: The id of the privacy amplification attempt or -1 if the
    amplification couldn't be attempted
    :rtype: int"""

    reconciliation = db.reconciliation[
        db.reconciliation[RecCols.ID] == reconciliation_id
    ]
    alice_raw: str = reconciliation[RecCols.ALICE_KEY].iloc[0]
    bob_raw: str = reconciliation[RecCols.BOB_KEY].iloc[0]

    if alice_raw == "" or bob_raw == "":
        return -1

    alice_key, bob_key = amplification_protocol.amplify_keys(
        base_16_to_base_2(alice_raw),
        base_16_to_base_2(bob_raw),
    )

    amplification_id = db.load_amplification(
        amplification_protocol.get_name(),
        reconciliation_id,
        base_2_to_base_16(alice_key),
        base_2_to_base_16(bob_key),
    )

    db.load_amplification_params(
        amplification_id,
        amplification_protocol.get_all_param_and_values(),
    )

    return amplification_id
