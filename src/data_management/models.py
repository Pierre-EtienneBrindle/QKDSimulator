"Module containing classes that simplify data recording and manipulation"

from typing import Callable, List, Dict, Any, Tuple
import pandas as pd

from src.data_management.schema import (
    DistributionProtocolColumns,
    RunColumns,
    DistributionParametersColumns,
    EnvironmentColumns,
    EnvironmentParametersColumns,
    RunLabelsColumns,
    RawMeasurementColumns,
    ReconciliationParametersColumns,
    ReconciliationColumns,
    ReconciliationProtocolColumns,
    AmplificationProtocolColumns,
    AmplificationColumns,
    AmplificationParametersColumns,
)
from src.distribution import DistributionProtocol, Environment
from src.reconciliation import ReconciliationProtocol
from src.amplification import AmplificationProtocol


class DataBase:
    """Class that stores the results of the different simulations and some
    logs inside DataFrames to simplify analysis and manipulations"""

    distribution_protocol: pd.DataFrame
    run: pd.DataFrame
    distribution_parameters: pd.DataFrame
    environment: pd.DataFrame
    environment_parameters: pd.DataFrame
    run_labels: pd.DataFrame
    raw_measurement: pd.DataFrame

    reconciliation_protocol: pd.DataFrame
    reconciliation: pd.DataFrame
    reconciliation_parameters: pd.DataFrame

    amplification_protocol: pd.DataFrame
    amplification: pd.DataFrame
    amplification_parameters: pd.DataFrame

    def __init__(self):

        self.distribution_protocol = pd.DataFrame(
            {
                DistributionProtocolColumns.NAME: pd.Series(dtype="string"),
                DistributionProtocolColumns.CONSTRUCTOR: pd.Series(
                    dtype="object"
                ),
            }
        )

        self.run = pd.DataFrame(
            {
                RunColumns.ID: pd.Series(dtype="uint32"),
                RunColumns.PROTOCOL_NAME: pd.Series(dtype="string"),
                RunColumns.ENVIRONMENT_NAME: pd.Series(dtype="string"),
            }
        )

        self.distribution_parameters = pd.DataFrame(
            {
                DistributionParametersColumns.RUN_ID: pd.Series(
                    dtype="uint32"
                ),
                DistributionParametersColumns.NAME: pd.Series(dtype="string"),
                DistributionParametersColumns.VALUE: pd.Series(
                    dtype="object"
                ),
            }
        )

        self.environment = pd.DataFrame(
            {
                EnvironmentColumns.NAME: pd.Series(dtype="string"),
                EnvironmentColumns.CONSTRUCTOR: pd.Series(dtype="object"),
            }
        )

        self.environment_parameters = pd.DataFrame(
            {
                EnvironmentParametersColumns.RUN_ID: pd.Series(
                    dtype="uint32"
                ),
                EnvironmentParametersColumns.NAME: pd.Series(dtype="string"),
                EnvironmentParametersColumns.VALUE: pd.Series(dtype="object"),
            }
        )

        self.run_labels = pd.DataFrame(
            {
                RunLabelsColumns.RUN_ID: pd.Series(dtype="uint32"),
                RunLabelsColumns.QBIT_NUM: pd.Series(dtype="uint8"),
                RunLabelsColumns.QBIT_LABEL: pd.Series(dtype="string"),
            }
        )

        self.raw_measurement = pd.DataFrame(
            {
                RawMeasurementColumns.RUN_ID: pd.Series(dtype="uint32"),
                RawMeasurementColumns.ITERATION: pd.Series(dtype="uint32"),
                RawMeasurementColumns.MEASUREMENT: pd.Series(dtype="string"),
            }
        )

        self.reconciliation_protocol = pd.DataFrame(
            {
                ReconciliationProtocolColumns.NAME: pd.Series(dtype="string"),
                ReconciliationProtocolColumns.CONSTRUCTOR: pd.Series(
                    dtype="object"
                ),
            }
        )

        self.reconciliation = pd.DataFrame(
            {
                ReconciliationColumns.ID: pd.Series(dtype="uint32"),
                ReconciliationColumns.PROTOCOL_NAME: pd.Series(
                    dtype="string"
                ),
                ReconciliationColumns.RUN_ID: pd.Series(dtype="uint32"),
                ReconciliationColumns.ALICE_KEY: pd.Series(dtype="string"),
                ReconciliationColumns.BOB_KEY: pd.Series(dtype="string"),
            }
        )

        self.reconciliation_parameters = pd.DataFrame(
            {
                ReconciliationParametersColumns.RECONCILIATION_ID: pd.Series(
                    dtype="uint32"
                ),
                ReconciliationParametersColumns.NAME: pd.Series(
                    dtype="string"
                ),
                ReconciliationParametersColumns.VALUE: pd.Series(
                    dtype="object"
                ),
            }
        )

        self.amplification_protocol = pd.DataFrame(
            {
                AmplificationProtocolColumns.NAME: pd.Series(dtype="string"),
                AmplificationProtocolColumns.CONSTRUCTOR: pd.Series(
                    dtype="object"
                ),
            }
        )

        self.amplification = pd.DataFrame(
            {
                AmplificationColumns.ID: pd.Series(dtype="uint32"),
                AmplificationColumns.PROTOCOL_NAME: pd.Series(dtype="string"),
                AmplificationColumns.RECONCILIATION_ID: pd.Series(
                    dtype="uint32"
                ),
                AmplificationColumns.ALICE_KEY: pd.Series(dtype="string"),
                AmplificationColumns.BOB_KEY: pd.Series(dtype="string"),
            }
        )

        self.amplification_parameters = pd.DataFrame(
            {
                AmplificationParametersColumns.AMPLIFICATION_ID: pd.Series(
                    dtype="uint32"
                ),
                AmplificationParametersColumns.NAME: pd.Series(
                    dtype="string"
                ),
                AmplificationParametersColumns.VALUE: pd.Series(
                    dtype="object"
                ),
            }
        )

    def load_run(self, protocol_name: str, environment_name: str) -> int:
        """Adds the run to the 'run' dataframe.

        :param protocol_name: The name of the protocol simulated
        :type protocol_name: str
        :param environment_name: The name of the environment that added noise
        to the system
        :type environment_name: str
        :return: The id of the run
        :rtype: int"""

        run_id = 0
        if len(self.run) > 0:
            run_id = self.run[RunColumns.ID].max() + 1

        temp = pd.DataFrame(
            [
                {
                    RunColumns.ID: run_id,
                    RunColumns.PROTOCOL_NAME: protocol_name,
                    RunColumns.ENVIRONMENT_NAME: environment_name,
                }
            ]
        )

        self.run = pd.concat([self.run, temp])
        return run_id

    def load_distribution_protocols(
        self,
        distribution_protocols: List[
            Tuple[str, Callable[[Dict[str, Any]], DistributionProtocol]]
        ],
    ) -> None:
        """Loads the distribution protocols inside the 'distribution_protocol' DataFrame

        :param distribution_protocols: The protocols to add to the DataFrame
        :type distribution_protocols:
        List[Tuple[str, Callable[[Dict[str, Any]], DistributionProtocol]]]
        """

        temp = pd.DataFrame(
            [
                {
                    DistributionProtocolColumns.NAME: item[0],
                    DistributionProtocolColumns.CONSTRUCTOR: item[1],
                }
                for item in distribution_protocols
            ]
        )

        self.distribution_protocol = pd.concat(
            [self.distribution_protocol, temp]
        ).drop_duplicates(
            subset=[DistributionProtocolColumns.NAME],
            keep="last",
        )

    def load_distribution_parameters(
        self, run_id: int, params: List[Tuple[str, Any]]
    ) -> None:
        """Adds the run parameters to the 'distribution_parameters' dataframe.

        :param run_id: The id of the run
        :type run_id: int
        :param params: All the params to add
        :type params: List[Tuple[str,Any]]"""

        temp = pd.DataFrame(
            [
                {
                    DistributionParametersColumns.RUN_ID: run_id,
                    DistributionParametersColumns.NAME: param[0],
                    DistributionParametersColumns.VALUE: param[1],
                }
                for param in params
            ]
        )

        self.distribution_parameters = pd.concat(
            [self.distribution_parameters, temp]
        ).drop_duplicates(
            subset=[
                DistributionParametersColumns.RUN_ID,
                DistributionParametersColumns.NAME,
            ],
            keep="first",
        )

    def load_environments(
        self,
        environments: List[
            Tuple[str, Callable[[Dict[str, Any], Environment]]]
        ],
    ) -> None:
        """Loads the environments inside the 'environment' DataFrame

        :param distribution_protocols: The environments to add to the
        DataFrame
        :type distribution_protocols:
        List[Tuple[str, Callable[[Dict[str, Any]], Environment]]]
        """
        temp = pd.DataFrame(
            [
                {
                    EnvironmentColumns.NAME: item[0],
                    EnvironmentColumns.CONSTRUCTOR: item[1],
                }
                for item in environments
            ]
        )

        self.environment = pd.concat(
            [self.environment, temp]
        ).drop_duplicates(subset=[EnvironmentColumns.NAME], keep="last")

    def load_environment_parameters(
        self, run_id: int, params: List[Tuple[str, Any]]
    ) -> None:
        """Adds the environment parameters to the
        'environment_parameters' dataframe.

        :param environment_id: The id of the run
        :type environment_id: int
        :param params: All the params to add
        :type params: List[Tuple[str,Any]]"""

        temp = pd.DataFrame(
            [
                {
                    EnvironmentParametersColumns.RUN_ID: run_id,
                    EnvironmentParametersColumns.NAME: param[0],
                    EnvironmentParametersColumns.VALUE: param[1],
                }
                for param in params
            ]
        )

        self.environment_parameters = pd.concat(
            [self.environment_parameters, temp]
        ).drop_duplicates(
            subset=[
                EnvironmentParametersColumns.RUN_ID,
                EnvironmentParametersColumns.NAME,
            ],
            keep="first",
        )

    def load_run_labels(self, run_id: int, labels: List[str]) -> None:
        """Adds the run labels in the 'run_labels' DataFrame. To conserve
        endianness, the labels are stored in the reverse order.

        :param run_id : The id of the run the labels are related to
        :type run_id: int
        :param labels: The name of each qbits
        :type labels: List[str]"""

        temp = pd.DataFrame(
            [
                {
                    RunLabelsColumns.RUN_ID: run_id,
                    RunLabelsColumns.QBIT_NUM: pos,
                    RunLabelsColumns.QBIT_LABEL: label,
                }
                for pos, label in enumerate(reversed(labels))
            ]
        )

        self.run_labels = pd.concat([self.run_labels, temp]).drop_duplicates(
            subset=[
                RunLabelsColumns.RUN_ID,
                RunLabelsColumns.QBIT_NUM,
            ],
            keep="first",
        )

    def load_raw_measurements(
        self, run_id: int, measurements: List[str]
    ) -> None:
        """Adds the measurement into the 'raw_measurement' DataFrame.

        :param run_id: The id of the run the measurements come from
        :type run_id: int
        :param measurements: The measurements collected
        :type measurements: List[str]"""

        temp = pd.DataFrame(
            [
                {
                    RawMeasurementColumns.RUN_ID: run_id,
                    RawMeasurementColumns.ITERATION: pos,
                    RawMeasurementColumns.MEASUREMENT: meas,
                }
                for pos, meas in enumerate(measurements)
            ]
        )

        self.raw_measurement = pd.concat(
            [self.raw_measurement, temp]
        ).drop_duplicates(
            subset=[
                RawMeasurementColumns.RUN_ID,
                RawMeasurementColumns.ITERATION,
            ],
            keep="first",
        )

    def load_reconciliation_protocols(
        self,
        reconciliation_protocols: List[
            Tuple[str, Callable[[Dict[str, Any]], ReconciliationProtocol]]
        ],
    ) -> None:
        """Loads the reconciliation protocols inside the 'reconciliation_protocol' DataFrame

        :param reconciliation_protocols: The protocols to add to the DataFrame
        :type reconciliation_protocols:
        List[Tuple[str, Callable[[Dict[str, Any]], ReconciliationProtocol]]]
        """

        temp = pd.DataFrame(
            [
                {
                    ReconciliationProtocolColumns.NAME: item[0],
                    ReconciliationProtocolColumns.CONSTRUCTOR: item[1],
                }
                for item in reconciliation_protocols
            ]
        )

        self.reconciliation_protocol = pd.concat(
            [self.reconciliation_protocol, temp]
        ).drop_duplicates(
            subset=[ReconciliationProtocolColumns.NAME],
            keep="last",
        )

    def load_reconciliation(
        self, protocol_name: str, run_id: int, alice_key: str, bob_key: str
    ) -> int:
        """Adds the reconciliation attempt into the 'reconciliation' data frame

        :param protocol_name: The name of the protocol
        :type protocol_name: str
        :param run_id: The id of the run they keys are based from
        :type run_id: int
        :param alice_key: The reconciled key from Alice
        :type alice_key: str
        :param bob_key: The reconciled key from Bob
        :type bob_key:
        :return: The reconciliation attempt's id
        :rtype: int"""

        reconciliation_id = 0

        if len(self.reconciliation) > 0:
            reconciliation_id = (
                self.reconciliation[ReconciliationColumns.ID].max() + 1
            )

        temp = pd.DataFrame(
            [
                {
                    ReconciliationColumns.ID: reconciliation_id,
                    ReconciliationColumns.PROTOCOL_NAME: protocol_name,
                    ReconciliationColumns.RUN_ID: run_id,
                    ReconciliationColumns.ALICE_KEY: alice_key,
                    ReconciliationColumns.BOB_KEY: bob_key,
                }
            ]
        )

        self.reconciliation = pd.concat([self.reconciliation, temp])

        return reconciliation_id

    def load_reconciliation_parameters(
        self, reconciliation_id: int, params: List[Tuple[str, Any]]
    ) -> None:
        """Adds the information reconciliation's protocol parameters inside
        the 'reconciliation_parameters' df.

        :param reconciliation_id: The id of the reconciliation attempt
        :type reconciliation_id: int
        :param params: The parameters of the reconciliation attempt
        :type params: List[Tuple[str,Any]]"""

        temp = pd.DataFrame(
            [
                {
                    ReconciliationParametersColumns.NAME: param[0],
                    ReconciliationParametersColumns.VALUE: param[1],
                    ReconciliationParametersColumns.RECONCILIATION_ID: reconciliation_id,
                }
                for param in params
            ]
        )

        self.reconciliation_parameters = pd.concat(
            [self.reconciliation_parameters, temp]
        ).drop_duplicates(
            subset=[
                ReconciliationParametersColumns.NAME,
                ReconciliationParametersColumns.RECONCILIATION_ID,
            ],
            keep="first",
        )

    def load_amplification_protocols(
        self,
        amplification_protocols: List[
            Tuple[str, Callable[[Dict[str, Any]], AmplificationProtocol]]
        ],
    ) -> None:
        """Loads the amplification protocols inside the 'amplification_protocol' DataFrame

        :param amplification_protocols: The protocols to add to the DataFrame
        :type amplification_protocols:
        List[Tuple[str, Callable[[Dict[str, Any]], AmplificationProtocol]]]
        """

        temp = pd.DataFrame(
            [
                {
                    AmplificationProtocolColumns.NAME: item[0],
                    AmplificationProtocolColumns.CONSTRUCTOR: item[1],
                }
                for item in amplification_protocols
            ]
        )

        self.amplification_protocol = pd.concat(
            [self.amplification_protocol, temp]
        ).drop_duplicates(
            subset=[AmplificationProtocolColumns.NAME],
            keep="last",
        )

    def load_amplification(
        self,
        protocol_name: str,
        reconciliation_id: int,
        alice_key: str,
        bob_key: str,
    ) -> int:
        """Adds the privacy amplification attempt to the 'amplification' df

        :param protocol_name: The privacy amplification protocol used
        :type protocol_name: str
        :param reconciliation_id: The id of the information reconciliation
        attempt where the keys come from
        :param reconciliation_id: int
        :param alice_key: Alice's amplified key
        :type alice_key: str
        :param bob_key: Bob's amplified key
        :type bob_key: str
        :return: The privacy amplification attempt's id
        :rtype: int"""

        amplification_id = 0

        if len(self.amplification) > 0:
            amplification_id = (
                self.amplification[AmplificationColumns.ID].max() + 1
            )

        temp = pd.DataFrame(
            {
                AmplificationColumns.ID: amplification_id,
                AmplificationColumns.PROTOCOL_NAME: protocol_name,
                AmplificationColumns.RECONCILIATION_ID: reconciliation_id,
                AmplificationColumns.ALICE_KEY: alice_key,
                AmplificationColumns.BOB_KEY: bob_key,
            }
        )

        self.amplification = pd.concat([self.amplification, temp])

        return amplification_id

    def load_amplification_parameters(
        self, amplification_id: int, params: List[str, Any]
    ) -> None:
        """Adds the privacy amplification attempt's parameter into the 'amplification_parameter' df

        :param amplification_id : The privacy amplification attempt's id
        :type amplification_id: int
        :param params: The parameters of the privacy amplification protocol
        used
        :type params: List[str,Any]"""

        temp = pd.DataFrame(
            [
                {
                    AmplificationParametersColumns.NAME: param[0],
                    AmplificationParametersColumns.VALUE: param[1],
                    AmplificationParametersColumns.AMPLIFICATION_ID: amplification_id,
                }
                for param in params
            ]
        )

        self.amplification_parameters = pd.concat(
            [self.amplification_parameters, temp]
        ).drop_duplicates(
            subset=[
                AmplificationParametersColumns.NAME,
                AmplificationParametersColumns.AMPLIFICATION_ID,
            ],
            keep="first",
        )
