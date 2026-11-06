"""Module that gives access to function to simulate a given privacy
amplification protocol"""

from src.amplification import AmplificationProtocol
from src.data_management import (
    DataBase,
    ReconciliationColumns,
)


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
    :return: The id of the privacy amplification attempt
    :rtype: int"""

    reconciliation = db.reconciliation[
        db.reconciliation[ReconciliationColumns.ID] == reconciliation_id
    ]
    alice_raw: str = reconciliation[ReconciliationColumns.ALICE_KEY].iloc[0]
    bob_raw: str = reconciliation[ReconciliationColumns.BOB_KEY].iloc[0]

    alice_key, bob_key = amplification_protocol.amplify_keys(
        alice_raw, bob_raw
    )

    amplification_id = db.load_amplification(
        amplification_protocol.get_name(),
        reconciliation_id,
        alice_key,
        bob_key,
    )

    db.load_amplification_parameters(
        amplification_id,
        amplification_protocol.get_all_params_names_and_values(),
    )

    return amplification_id
