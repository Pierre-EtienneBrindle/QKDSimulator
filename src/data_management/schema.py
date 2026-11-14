"""Module containing enums that simplify addressing dataframe's rows and
columns and accessing the correct files"""

from enum import StrEnum, auto


class DistProtCols(StrEnum):
    """Enumeration of all the columns of the df 'distribution_protocol'"""

    NAME = auto()
    CONSTRUCTOR = auto()


class RunCols(StrEnum):
    """Enumeration of all the columns of the df 'run'"""

    ID = auto()
    PROTOCOL_NAME = auto()
    ENVIRONMENT_NAME = auto()
    ALICE_KEY = auto()
    BOB_KEY = auto()
    EVE_INFO = auto()
    ERROR_RATE = auto()
    NUM_ITERATIONS = auto()


class DistParamsCols(StrEnum):
    """Enumeration of all the columns of the df 'distribution_params'"""

    RUN_ID = auto()
    NAME = auto()
    VALUE = auto()


class EnvCols(StrEnum):
    """Enumeration of all the columns of the df 'environment'"""

    NAME = auto()
    CONSTRUCTOR = auto()


class EnvParamsCols(StrEnum):
    """Enumeration of all the columns of the df 'environment_params'"""

    RUN_ID = auto()
    NAME = auto()
    VALUE = auto()


class RecProtCols(StrEnum):
    """Enumeration of all the columns of the df 'reconciliation_protocol'"""

    NAME = auto()
    CONSTRUCTOR = auto()


class RecCols(StrEnum):
    """Enumeration of all the columns of the df 'reconciliation'"""

    ID = auto()
    PROTOCOL_NAME = auto()
    RUN_ID = auto()
    ALICE_KEY = auto()
    BOB_KEY = auto()


class RecParamsCols(StrEnum):
    """Enumeration of all the columns of the df 'reconciliation_params'"""

    RECONCILIATION_ID = auto()
    NAME = auto()
    VALUE = auto()


class AmpProtCols(StrEnum):
    """Enumeration of all the columns of the df 'amplification_protocol'"""

    NAME = auto()
    CONSTRUCTOR = auto()


class AmpCols(StrEnum):
    """Enumeration of all the columns of the df 'amplification'"""

    ID = auto()
    PROTOCOL_NAME = auto()
    RECONCILIATION_ID = auto()
    ALICE_KEY = auto()
    BOB_KEY = auto()


class AmpParamsCols(StrEnum):
    """Enumeration of all the columns of the df 'amplification_params'"""

    AMPLIFICATION_ID = auto()
    NAME = auto()
    VALUE = auto()


class DataBaseFileNames(StrEnum):
    """Enumeration of all the names of the files that the database saves to"""

    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        # Adds .json to every enum item
        return name.lower() + ".json"

    RUN = auto()
    DISTRIBUTION_PARAMETERS = auto()
    ENVIRONMENT_PARAMETERS = auto()
    RECONCILIATION = auto()
    RECONCILIATION_PARAMETERS = auto()
    AMPLIFICATION = auto()
    AMPLIFICATION_PARAMETERS = auto()
