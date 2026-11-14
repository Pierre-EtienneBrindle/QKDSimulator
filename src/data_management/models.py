"Module containing classes that simplify data recording and manipulation"

from typing import List, Any, Tuple
import pandas as pd

from src.data_management.schema import (
    DistProtCols,
    RunCols,
    DistParamsCols,
    EnvCols,
    EnvParamsCols,
    RecParamsCols,
    RecCols,
    RecProtCols,
    AmpProtCols,
    AmpCols,
    AmpParamsCols,
)
from src.distribution import DistributionProtocol, Environment
from src.reconciliation import ReconciliationProtocol
from src.amplification import AmplificationProtocol


class DataBase:
    """Class that stores the results of the different simulations and some
    logs inside DataFrames to simplify analysis and manipulations"""

    distribution_protocol: pd.DataFrame
    run: pd.DataFrame
    distribution_params: pd.DataFrame
    environment: pd.DataFrame
    environment_params: pd.DataFrame

    reconciliation_protocol: pd.DataFrame
    reconciliation: pd.DataFrame
    reconciliation_params: pd.DataFrame

    amplification_protocol: pd.DataFrame
    amplification: pd.DataFrame
    amplification_params: pd.DataFrame

    def __init__(self):

        self.distribution_protocol = pd.DataFrame(
            {
                DistProtCols.NAME: pd.Series(dtype="string"),
                DistProtCols.CONSTRUCTOR: pd.Series(dtype="object"),
            }
        )

        self.run = pd.DataFrame(
            {
                RunCols.ID: pd.Series(dtype="uint32"),
                RunCols.PROTOCOL_NAME: pd.Series(dtype="string"),
                RunCols.ENVIRONMENT_NAME: pd.Series(dtype="string"),
                RunCols.ALICE_KEY: pd.Series(dtype="string"),
                RunCols.BOB_KEY: pd.Series(dtype="string"),
                RunCols.EVE_INFO: pd.Series(dtype="string"),
                RunCols.ERROR_RATE: pd.Series(dtype="float64"),
                RunCols.NUM_ITERATIONS: pd.Series(dtype="uint32"),
            }
        )

        self.distribution_params = pd.DataFrame(
            {
                DistParamsCols.RUN_ID: pd.Series(dtype="uint32"),
                DistParamsCols.NAME: pd.Series(dtype="string"),
                DistParamsCols.VALUE: pd.Series(dtype="object"),
            }
        )

        self.environment = pd.DataFrame(
            {
                EnvCols.NAME: pd.Series(dtype="string"),
                EnvCols.CONSTRUCTOR: pd.Series(dtype="object"),
            }
        )

        self.environment_params = pd.DataFrame(
            {
                EnvParamsCols.RUN_ID: pd.Series(dtype="uint32"),
                EnvParamsCols.NAME: pd.Series(dtype="string"),
                EnvParamsCols.VALUE: pd.Series(dtype="object"),
            }
        )

        self.reconciliation_protocol = pd.DataFrame(
            {
                RecProtCols.NAME: pd.Series(dtype="string"),
                RecProtCols.CONSTRUCTOR: pd.Series(dtype="object"),
            }
        )

        self.reconciliation = pd.DataFrame(
            {
                RecCols.ID: pd.Series(dtype="uint32"),
                RecCols.PROTOCOL_NAME: pd.Series(dtype="string"),
                RecCols.RUN_ID: pd.Series(dtype="uint32"),
                RecCols.ALICE_KEY: pd.Series(dtype="string"),
                RecCols.BOB_KEY: pd.Series(dtype="string"),
            }
        )

        self.reconciliation_params = pd.DataFrame(
            {
                RecParamsCols.RECONCILIATION_ID: pd.Series(dtype="uint32"),
                RecParamsCols.NAME: pd.Series(dtype="string"),
                RecParamsCols.VALUE: pd.Series(dtype="object"),
            }
        )

        self.amplification_protocol = pd.DataFrame(
            {
                AmpProtCols.NAME: pd.Series(dtype="string"),
                AmpProtCols.CONSTRUCTOR: pd.Series(dtype="object"),
            }
        )

        self.amplification = pd.DataFrame(
            {
                AmpCols.ID: pd.Series(dtype="uint32"),
                AmpCols.PROTOCOL_NAME: pd.Series(dtype="string"),
                AmpCols.RECONCILIATION_ID: pd.Series(dtype="uint32"),
                AmpCols.ALICE_KEY: pd.Series(dtype="string"),
                AmpCols.BOB_KEY: pd.Series(dtype="string"),
            }
        )

        self.amplification_params = pd.DataFrame(
            {
                AmpParamsCols.AMPLIFICATION_ID: pd.Series(dtype="uint32"),
                AmpParamsCols.NAME: pd.Series(dtype="string"),
                AmpParamsCols.VALUE: pd.Series(dtype="object"),
            }
        )

    def load_run(
        self,
        protocol_name: str,
        environment_name: str,
        alice_key: str,
        bob_key: str,
        eve_info: str,
        error_rate: float,
        num_iterations: int,
    ) -> int:
        """Adds the run to the 'run' dataframe.

        :param protocol_name: The name of the protocol simulated
        :type protocol_name: str
        :param environment_name: The name of the environment that added noise
        to the system
        :type environment_name: str
        :param alice_key: Alice's raw key obtained in the run
        :type alice_key: str
        :param bob_key: Bob's raw key obtained in the run
        :type bob_key: str
        :param eve_info: Informations on the key obtained by Eve
        :type eve_info: str
        :param error_rate : The detected error rate
        :type error_rate: float
        :param num_iterations: The number of iterations done to get the key
        :type num_iterations: int
        :return: The id of the run
        :rtype: int"""

        run_id = 0
        if len(self.run) > 0:
            run_id = self.run[RunCols.ID].max() + 1

        temp = pd.DataFrame(
            [
                {
                    RunCols.ID: run_id,
                    RunCols.PROTOCOL_NAME: protocol_name,
                    RunCols.ENVIRONMENT_NAME: environment_name,
                    RunCols.ALICE_KEY: alice_key,
                    RunCols.BOB_KEY: bob_key,
                    RunCols.EVE_INFO: eve_info,
                    RunCols.ERROR_RATE: error_rate,
                    RunCols.NUM_ITERATIONS: num_iterations,
                }
            ]
        )

        self.run = pd.concat([self.run, temp])
        return run_id

    def load_distribution_protocols(
        self,
        distribution_protocols: List[type[DistributionProtocol]],
    ) -> None:
        """Loads the distribution protocols inside the
        'distribution_protocol' DataFrame

        :param distribution_protocols: The protocols to add to the DataFrame
        :type distribution_protocols: List[type[DistributionProtocol]]
        """

        temp = pd.DataFrame(
            [
                {
                    DistProtCols.NAME: prot.get_name(),
                    DistProtCols.CONSTRUCTOR: prot.get_instance_from_params,
                }
                for prot in distribution_protocols
            ]
        )

        self.distribution_protocol = pd.concat(
            [self.distribution_protocol, temp]
        ).drop_duplicates(
            subset=[DistProtCols.NAME],
            keep="last",
        )

    def load_distribution_params(
        self, run_id: int, params: List[Tuple[str, Any]]
    ) -> None:
        """Adds the run parameters to the 'distribution_params' dataframe.

        :param run_id: The id of the run
        :type run_id: int
        :param params: All the params to add
        :type params: List[Tuple[str,Any]]"""

        temp = pd.DataFrame(
            [
                {
                    DistParamsCols.RUN_ID: run_id,
                    DistParamsCols.NAME: param[0],
                    DistParamsCols.VALUE: param[1],
                }
                for param in params
            ]
        )

        self.distribution_params = pd.concat(
            [self.distribution_params, temp]
        ).drop_duplicates(
            subset=[
                DistParamsCols.RUN_ID,
                DistParamsCols.NAME,
            ],
            keep="first",
        )

    def load_environments(
        self,
        environments: List[type[Environment]],
    ) -> None:
        """Loads the environments inside the 'environment' DataFrame

        :param distribution_protocols: The environments to add to the
        DataFrame
        :type distribution_protocols: List[type[Environment]]
        """
        temp = pd.DataFrame(
            [
                {
                    EnvCols.NAME: env.get_name(),
                    EnvCols.CONSTRUCTOR: env.get_instance_from_params,
                }
                for env in environments
            ]
        )

        self.environment = pd.concat(
            [self.environment, temp]
        ).drop_duplicates(subset=[EnvCols.NAME], keep="last")

    def load_environment_params(
        self, run_id: int, params: List[Tuple[str, Any]]
    ) -> None:
        """Adds the environment parameters to the
        'environment_params' dataframe.

        :param environment_id: The id of the run
        :type environment_id: int
        :param params: All the params to add
        :type params: List[Tuple[str,Any]]"""

        temp = pd.DataFrame(
            [
                {
                    EnvParamsCols.RUN_ID: run_id,
                    EnvParamsCols.NAME: param[0],
                    EnvParamsCols.VALUE: param[1],
                }
                for param in params
            ]
        )

        self.environment_params = pd.concat(
            [self.environment_params, temp]
        ).drop_duplicates(
            subset=[
                EnvParamsCols.RUN_ID,
                EnvParamsCols.NAME,
            ],
            keep="first",
        )

    def load_reconciliation_protocols(
        self,
        reconciliation_protocols: List[type[ReconciliationProtocol]],
    ) -> None:
        """Loads the reconciliation protocols inside the 'reconciliation_protocol' DataFrame

        :param reconciliation_protocols: The protocols to add to the DataFrame
        :type reconciliation_protocols:  List[type[ReconciliationProtocol]]
        """

        temp = pd.DataFrame(
            [
                {
                    RecProtCols.NAME: prot.get_name(),
                    RecProtCols.CONSTRUCTOR: prot.get_instance_from_params,
                }
                for prot in reconciliation_protocols
            ]
        )

        self.reconciliation_protocol = pd.concat(
            [self.reconciliation_protocol, temp]
        ).drop_duplicates(
            subset=[RecProtCols.NAME],
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
            reconciliation_id = self.reconciliation[RecCols.ID].max() + 1

        temp = pd.DataFrame(
            [
                {
                    RecCols.ID: reconciliation_id,
                    RecCols.PROTOCOL_NAME: protocol_name,
                    RecCols.RUN_ID: run_id,
                    RecCols.ALICE_KEY: alice_key,
                    RecCols.BOB_KEY: bob_key,
                }
            ]
        )

        self.reconciliation = pd.concat([self.reconciliation, temp])

        return reconciliation_id

    def load_reconciliation_params(
        self, reconciliation_id: int, params: List[Tuple[str, Any]]
    ) -> None:
        """Adds the information reconciliation's protocol parameters inside
        the 'reconciliation_params' df.

        :param reconciliation_id: The id of the reconciliation attempt
        :type reconciliation_id: int
        :param params: The parameters of the reconciliation attempt
        :type params: List[Tuple[str,Any]]"""

        temp = pd.DataFrame(
            [
                {
                    RecParamsCols.NAME: param[0],
                    RecParamsCols.VALUE: param[1],
                    RecParamsCols.RECONCILIATION_ID: reconciliation_id,
                }
                for param in params
            ]
        )

        self.reconciliation_params = pd.concat(
            [self.reconciliation_params, temp]
        ).drop_duplicates(
            subset=[
                RecParamsCols.NAME,
                RecParamsCols.RECONCILIATION_ID,
            ],
            keep="first",
        )

    def load_amplification_protocols(
        self,
        amplification_protocols: List[type[AmplificationProtocol]],
    ) -> None:
        """Loads the amplification protocols inside the 'amplification_protocol' DataFrame

        :param amplification_protocols: The protocols to add to the DataFrame
        :type amplification_protocols: List[type[AmplificationProtocol]]
        """

        temp = pd.DataFrame(
            [
                {
                    AmpProtCols.NAME: prot.get_name(),
                    AmpProtCols.CONSTRUCTOR: prot.get_instance_from_params,
                }
                for prot in amplification_protocols
            ]
        )

        self.amplification_protocol = pd.concat(
            [self.amplification_protocol, temp]
        ).drop_duplicates(
            subset=[AmpProtCols.NAME],
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
            amplification_id = self.amplification[AmpCols.ID].max() + 1

        temp = pd.DataFrame(
            {
                AmpCols.ID: amplification_id,
                AmpCols.PROTOCOL_NAME: protocol_name,
                AmpCols.RECONCILIATION_ID: reconciliation_id,
                AmpCols.ALICE_KEY: alice_key,
                AmpCols.BOB_KEY: bob_key,
            }
        )

        self.amplification = pd.concat([self.amplification, temp])

        return amplification_id

    def load_amplification_params(
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
                    AmpParamsCols.NAME: param[0],
                    AmpParamsCols.VALUE: param[1],
                    AmpParamsCols.AMPLIFICATION_ID: amplification_id,
                }
                for param in params
            ]
        )

        self.amplification_params = pd.concat(
            [self.amplification_params, temp]
        ).drop_duplicates(
            subset=[
                AmpParamsCols.NAME,
                AmpParamsCols.AMPLIFICATION_ID,
            ],
            keep="first",
        )
