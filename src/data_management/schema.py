"""Module containing enums that simplify addressing dataframe's rows and
columns and accessing the correct files"""

from enum import StrEnum, auto


class DistributionProtocolColumns(StrEnum):
    """Enumeration of all the columns of the df 'distribution_protocol'"""

    NAME = auto()
    CONSTRUCTOR = auto()


class RunColumns(StrEnum):
    """Enumeration of all the columns of the df 'run'"""

    ID = auto()
    PROTOCOL_NAME = auto()
    ENVIRONMENT_NAME = auto()


class DistributionParametersColumns(StrEnum):
    """Enumeration of all the columns of the df 'distribution_parameters'"""

    RUN_ID = auto()
    NAME = auto()
    VALUE = auto()


class EnvironmentColumns(StrEnum):
    """Enumeration of all the columns of the df 'environment'"""

    NAME = auto()
    CONSTRUCTOR = auto()


class EnvironmentParametersColumns(StrEnum):
    """Enumeration of all the columns of the df 'environment_parameters'"""

    RUN_ID = auto()
    NAME = auto()
    VALUE = auto()


class RunLabelsColumns(StrEnum):
    """Enumeration of all the columns of the df 'run_label'"""

    RUN_ID = auto()
    QBIT_NUM = auto()
    QBIT_LABEL = auto()


class RawMeasurementColumns(StrEnum):
    """Enumeration of all the columns of the df 'raw_measurement'"""

    RUN_ID = auto()
    ITERATION = auto()
    MEASUREMENT = auto()


class ReconciliationProtocolColumns(StrEnum):
    """Enumeration of all the columns of the df 'reconciliation_protocol'"""

    NAME = auto()
    CONSTRUCTOR = auto()


class ReconciliationColumns(StrEnum):
    """Enumeration of all the columns of the df 'reconciliation'"""

    ID = auto()
    PROTOCOL_NAME = auto()
    RUN_ID = auto()
    ALICE_KEY = auto()
    BOB_KEY = auto()


class ReconciliationParametersColumns(StrEnum):
    """Enumeration of all the columns of the df 'reconciliation_parameters'"""

    RECONCILIATION_ID = auto()
    NAME = auto()
    VALUE = auto()


class AmplificationProtocolColumns(StrEnum):
    """Enumeration of all the columns of the df 'amplification_protocol'"""

    NAME = auto()
    CONSTRUCTOR = auto()


class AmplificationColumns(StrEnum):
    """Enumeration of all the columns of the df 'amplification'"""

    ID = auto()
    PROTOCOL_NAME = auto()
    RECONCILIATION_ID = auto()
    ALICE_KEY = auto()
    BOB_KEY = auto()


class AmplificationParametersColumns(StrEnum):
    """Enumeration of all the columns of the df 'amplification_parameters'"""

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
    RUN_LABELS = auto()
    RAW_MEASUREMENTS = auto()
    RECONCILIATION = auto()
    RECONCILIATION_PARAMETERS = auto()
    AMPLIFICATION = auto()
    AMPLIFICATION_PARAMETERS = auto()
