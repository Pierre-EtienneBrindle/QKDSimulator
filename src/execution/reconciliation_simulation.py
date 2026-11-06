"""Module that gives access to function to simulate a given information
reconciliation protocol"""

from typing import Callable, Dict, Any, List
from src.reconciliation import ReconciliationProtocol
from src.data_management import (
    DataBase,
    RunColumns,
    DistributionProtocolColumns,
    DistributionParametersColumns,
    RunLabelsColumns,
    RawMeasurementColumns,
)
from src.distribution import DistributionProtocol


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

    dist_protocol_name: str = db.run[db.run[RunColumns.ID] == run_id][
        RunColumns.PROTOCOL_NAME
    ].iloc[0]

    constructor: Callable[[Dict[str, Any]], DistributionProtocol] = (
        db.distribution_protocol[
            db.distribution_protocol[DistributionProtocolColumns.NAME]
            == dist_protocol_name
        ][DistributionProtocolColumns.CONSTRUCTOR].iloc[0]
    )

    parameters = db.distribution_parameters[
        db.distribution_parameters[DistributionParametersColumns.RUN_ID]
        == run_id
    ]
    parameters: Dict[str, Any] = dict(
        zip(
            parameters[DistributionParametersColumns.NAME],
            parameters[DistributionParametersColumns.VALUE],
        )
    )

    labels: List[str] = list(
        db.run_labels[
            db.run_labels[RunLabelsColumns.RUN_ID] == run_id
        ].sort_values(by=RunLabelsColumns.QUBIT_NUM)[
            RunLabelsColumns.QUBIT_LABEL
        ]
    )
    measurements: List[str] = list(
        db.raw_measurement[
            db.raw_measurement[RawMeasurementColumns.RUN_ID] == run_id
        ].sort_values(by=RawMeasurementColumns.ITERATION)[
            RawMeasurementColumns.MEASUREMENT
        ]
    )

    dist_protocol = constructor(parameters)
    alice_raw, bob_raw = dist_protocol.compute_raw_keys(measurements, labels)

    alice_key, bob_key = reconciliation_protocol.reconciliate_keys(
        alice_raw, bob_raw
    )

    reconciliation_id = db.load_reconciliation(
        reconciliation_protocol.get_name(), run_id, alice_key, bob_key
    )

    db.load_reconciliation_parameters(
        reconciliation_id,
        reconciliation_protocol.get_all_params_names_and_values(),
    )

    return reconciliation_id
