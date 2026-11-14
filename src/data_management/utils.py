"""Module containing utility functions for the data management"""

from pathlib import Path

import pandas as pd

from src.data_management.models import DataBase
from src.data_management.schema import DataBaseFileNames


def save_db_in_folder(db: DataBase, folder_path: Path) -> None:
    """Saves the content of the database into a given folder. Does not save
    table with function pointers (distribution_protocol_info,
    environment_info, reconciliation_protocol_info and
    amplification_protocol_info).

    :param db: The database to serialize
    :type db: DataBase
    :param folder_path: The path to the folder to save data into
    :type folder_path: Path"""

    db.run.to_json(
        folder_path / DataBaseFileNames.RUN,
        orient="table",
        indent=4,
    )
    db.distribution_params.to_json(
        folder_path / DataBaseFileNames.DISTRIBUTION_PARAMETERS,
        orient="table",
        indent=4,
    )
    db.environment_params.to_json(
        folder_path / DataBaseFileNames.ENVIRONMENT_PARAMETERS,
        orient="table",
        indent=4,
    )

    db.reconciliation.to_json(
        folder_path / DataBaseFileNames.RECONCILIATION,
        orient="table",
        indent=4,
    )
    db.reconciliation_params.to_json(
        folder_path / DataBaseFileNames.RECONCILIATION_PARAMETERS,
        orient="table",
        indent=4,
    )

    db.amplification.to_json(
        folder_path / DataBaseFileNames.AMPLIFICATION,
        orient="table",
        indent=4,
    )
    db.amplification_params.to_json(
        folder_path / DataBaseFileNames.AMPLIFICATION_PARAMETERS,
        orient="table",
        indent=4,
    )


def load_db_from_folder(folder_path: Path) -> DataBase:
    """Loads in a database from the files inside a given folder. Does not
    load table with function pointers (distribution_protocol_info,
    environment_info, reconciliation_protocol_info and
    amplification_protocol_info).

    :param folder_path: The path to the folder to load the data from
    :type folder_path: Path
    :return: The loaded database
    :rtype: DataBase"""

    db = DataBase()

    db.run = pd.read_json(folder_path / DataBaseFileNames.RUN, orient="table")
    db.distribution_params = pd.read_json(
        folder_path / DataBaseFileNames.DISTRIBUTION_PARAMETERS,
        orient="table",
    )
    db.environment_params = pd.read_json(
        folder_path / DataBaseFileNames.ENVIRONMENT_PARAMETERS,
        orient="table",
    )

    db.reconciliation = pd.read_json(
        folder_path / DataBaseFileNames.RECONCILIATION,
        orient="table",
    )
    db.reconciliation_params = pd.read_json(
        folder_path / DataBaseFileNames.RECONCILIATION_PARAMETERS,
        orient="table",
    )

    db.amplification = pd.read_json(
        folder_path / DataBaseFileNames.AMPLIFICATION,
        orient="table",
    )
    db.amplification_params = pd.read_json(
        folder_path / DataBaseFileNames.AMPLIFICATION_PARAMETERS,
        orient="table",
    )

    return db
