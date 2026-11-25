"""Module that gives access to function to simulate a given privacy
amplification protocol"""

from src.distribution import DistributionProtocol
from src.amplification import AmplificationProtocol
from src.data_management import (
    DataBase,
    RecCols,
    RunCols,
    DistParamsCols,
    DistProtCols,
)
from src.execution.utils import compress_string, decompress_string


def get_protocol_and_error_rate(
    db: DataBase,
    run_id: int,
) -> tuple[DistributionProtocol, float]:
    """
    Instantiates the protocol and finds the run's error rate based on the run
    id.

    :param db: The database to check in
    :type db: Database
    :param run_id: The id of the run we're getting data from
    :type run_id: int
    :return: The instance of the protocol and the error rate
    :rtype: DistributionProtocol, float
    """

    run = db.run[db.run[RunCols.ID] == run_id]

    dist_prot_name: str = run[RunCols.PROTOCOL_NAME].iloc[0]
    constructor: callable = db.distribution_protocol[
        db.distribution_protocol[DistProtCols.NAME] == dist_prot_name
    ][DistProtCols.CONSTRUCTOR].iloc[0]

    params = db.distribution_params[
        db.distribution_params[DistParamsCols.RUN_ID] == run_id
    ]
    params = dict(
        zip(params[DistParamsCols.NAME], params[DistParamsCols.VALUE])
    )

    return constructor(params), run[RunCols.ERROR_RATE].iloc[0]


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
    nb_revealed: int = reconciliation[RecCols.NB_REVEALED].iloc[0]

    if alice_raw == "" or bob_raw == "":
        return -1

    protocol, error_rate = get_protocol_and_error_rate(
        db,
        reconciliation[RecCols.RUN_ID].iloc[0],
    )

    max_key_length = protocol.get_max_key_length(error_rate, nb_revealed)

    alice_key, bob_key = amplification_protocol.amplify_keys(
        decompress_string(alice_raw),
        decompress_string(bob_raw),
        max_key_length,
    )

    amplification_id = db.load_amplification(
        amplification_protocol.get_name(),
        reconciliation_id,
        compress_string(alice_key),
        compress_string(bob_key),
    )

    db.load_amplification_params(
        amplification_id,
        amplification_protocol.get_all_param_and_values(),
    )

    return amplification_id
