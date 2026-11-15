"""Module containing utility functions for the data management"""

from pathlib import Path

import pandas as pd

from src.data_management.models import DataBase
from src.data_management.schema import (
    DataBaseFileNames,
    RunCols,
    AmpCols,
    RecCols,
    AmpParamsCols,
    EnvParamsCols,
    RecParamsCols,
    DistParamsCols,
)


def check_if_folder_is_correct(folder_path: Path) -> bool:
    """
    Checks if the folder contains the correct files

    :param folder_path: The path of the folder to check
    :type folder_path: Path
    :returns: Whether the folder path given is setup to save data
    :rtype: bool"""

    if not folder_path.exists() or not folder_path.is_dir():
        return False

    for fn in DataBaseFileNames:
        file_path = folder_path / fn
        if not file_path.exists():
            return False

    return True


def setup_folder(folder_path: Path) -> None:
    """
    Setups the folder for data management

    :param folder_path: The path of the folder to setup
    :type folder_path: Path"""
    if folder_path.exists() and not folder_path.is_dir():
        raise ValueError(
            f"The given path is not a folder path. Path given : {folder_path}"
        )

    folder_path.mkdir(parents=True, exist_ok=True)

    # Create dummy database
    save_db_in_folder(DataBase(), folder_path)


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
        orient="split",
        indent=4,
        index=False,
    )
    db.distribution_params.to_json(
        folder_path / DataBaseFileNames.DISTRIBUTION_PARAMETERS,
        orient="split",
        indent=4,
        index=False,
    )
    db.environment_params.to_json(
        folder_path / DataBaseFileNames.ENVIRONMENT_PARAMETERS,
        orient="split",
        indent=4,
        index=False,
    )

    db.reconciliation.to_json(
        folder_path / DataBaseFileNames.RECONCILIATION,
        orient="split",
        indent=4,
        index=False,
    )
    db.reconciliation_params.to_json(
        folder_path / DataBaseFileNames.RECONCILIATION_PARAMETERS,
        orient="split",
        indent=4,
        index=False,
    )

    db.amplification.to_json(
        folder_path / DataBaseFileNames.AMPLIFICATION,
        orient="split",
        indent=4,
        index=False,
    )
    db.amplification_params.to_json(
        folder_path / DataBaseFileNames.AMPLIFICATION_PARAMETERS,
        orient="split",
        indent=4,
        index=False,
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

    db.run = pd.read_json(
        folder_path / DataBaseFileNames.RUN,
        orient="split",
        dtype={
            RunCols.ID: "uint32",
            RunCols.PROTOCOL_NAME: "string",
            RunCols.ENVIRONMENT_NAME: "string",
            RunCols.ALICE_KEY: "string",
            RunCols.BOB_KEY: "string",
            RunCols.EVE_INFO: "string",
            RunCols.ERROR_RATE: "float64",
            RunCols.NUM_ITERATIONS: "uint32",
        },
    )
    db.distribution_params = pd.read_json(
        folder_path / DataBaseFileNames.DISTRIBUTION_PARAMETERS,
        orient="split",
        dtype={
            DistParamsCols.NAME: "string",
            DistParamsCols.RUN_ID: "uint32",
            DistParamsCols.VALUE: "object",
        },
    )
    db.environment_params = pd.read_json(
        folder_path / DataBaseFileNames.ENVIRONMENT_PARAMETERS,
        orient="split",
        dtype={
            EnvParamsCols.RUN_ID: "uint32",
            EnvParamsCols.NAME: "string",
            EnvParamsCols.VALUE: "object",
        },
    )

    db.reconciliation = pd.read_json(
        folder_path / DataBaseFileNames.RECONCILIATION,
        orient="split",
        dtype={
            RecCols.ID: "uint32",
            RecCols.PROTOCOL_NAME: "string",
            RecCols.RUN_ID: "uint32",
            RecCols.ALICE_KEY: "string",
            RecCols.BOB_KEY: "string",
        },
    )
    db.reconciliation_params = pd.read_json(
        folder_path / DataBaseFileNames.RECONCILIATION_PARAMETERS,
        orient="split",
        dtype={
            RecParamsCols.RECONCILIATION_ID: "uint32",
            RecParamsCols.NAME: "string",
            RecParamsCols.VALUE: "object",
        },
    )

    db.amplification = pd.read_json(
        folder_path / DataBaseFileNames.AMPLIFICATION,
        orient="split",
        dtype={
            AmpCols.ID: "uint32",
            AmpCols.PROTOCOL_NAME: "string",
            AmpCols.RECONCILIATION_ID: "uint32",
            AmpCols.ALICE_KEY: "string",
            AmpCols.BOB_KEY: "string",
        },
    )
    db.amplification_params = pd.read_json(
        folder_path / DataBaseFileNames.AMPLIFICATION_PARAMETERS,
        orient="split",
        dtype={
            AmpParamsCols.AMPLIFICATION_ID: "uint32",
            AmpParamsCols.NAME: "string",
            AmpParamsCols.VALUE: "object",
        },
    )

    return db
