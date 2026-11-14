"""Module giving access to function to execute distribution more easily"""

from src.distribution import System, Environment, DistributionProtocol
from src.data_management import DataBase


def compute_final_system(
    protocol: DistributionProtocol,
    environment: Environment,
) -> System:
    """Computes the final system after executing the protocol under the
    noise caused by the environment

    :param protocol: The protocol to simulate
    :type protocol: DistributionProtocol
    :param environment: The environment causing noise
    :type environment: Environment
    :return: The system after the protocol and environment were executed
    :rtype : System
    """

    final_system = System()
    for segment in range(protocol.get_num_segments()):
        final_system, transmitted_qbits = protocol.apply_protocol_segment(
            segment, final_system
        )

        final_system = environment.apply_environment_after_segment(
            segment,
            final_system,
            transmitted_qbits,
        )

    return final_system


def execute_run_and_store(
    protocol: DistributionProtocol, environment: Environment, db: DataBase
) -> int:
    """Measures the system and stores the result for each qbit

    :param protocol: The protocol to simulate
    :type protocol: DistributionProtocol
    :param environment: The environment causing noise
    :type environment: Environment
    :param db: The database to store the results inside of
    :type db: DataBase
    :param num_iterations: The number of iteration of the protocol to
    compute
    :return: The run_id of this execution to be able to get back the
    results
    :rtype: int"""

    system = compute_final_system(protocol, environment)
    labels = system.labels[::-1]

    measurements = []
    while not protocol.is_done(measurements, labels):
        measurements.append(system.state.measure()[0])

    alice_key, bob_key, error_rate = protocol.compute_raw_keys(
        measurements, labels
    )

    eve_info = ""
    if environment.is_eve():
        eve_info = environment.compute_eve_info(measurements, labels)

    run_id = db.load_run(
        protocol.get_name(),
        environment.get_name(),
        alice_key,
        bob_key,
        eve_info,
        error_rate,
        len(measurements),
    )
    db.load_distribution_params(
        run_id,
        protocol.get_all_param_and_values(),
    )
    db.load_environment_params(
        run_id,
        environment.get_all_param_and_values(),
    )
    db.load_run_labels(run_id, labels)

    return run_id
