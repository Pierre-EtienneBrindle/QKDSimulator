"""Module that gives access to function to simulate a given information
reconciliation protocol"""

from src.reconciliation import ReconciliationProtocol
from src.data_management import DataBase, RunCols


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
    :return: The id of the reconciliation attempt
    :rtype: int"""

    run_info = db.run[db.run[RunCols.ID] == run_id]
    alice_raw: str = run_info[RunCols.ALICE_KEY].iloc[0]
    bob_raw: str = run_info[RunCols.BOB_KEY].iloc[0]
    error_rate: float = run_info[RunCols.ERROR_RATE].iloc[0]

    alice_key, bob_key = reconciliation_protocol.reconciliate_keys(
        alice_raw,
        bob_raw,
        error_rate,
    )

    reconciliation_id = db.load_reconciliation(
        reconciliation_protocol.get_name(),
        run_id,
        alice_key,
        bob_key,
    )

    db.load_reconciliation_params(
        reconciliation_id,
        reconciliation_protocol.get_all_param_and_values(),
    )

    return reconciliation_id
