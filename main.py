"""Main code setup for data collection -- WILL BE CHANGED"""

from pathlib import Path
import numpy as np

from src.distribution import (
    DistributionProtocol,
    Environment,
    BB84KeyDistribution,
    TomamichelEtAlKeyDistribution,
    NoiselessEnvironment,
    SingleQbitAmplitudeDamping,
    SingleQbitDepolarization,
    BB84Eve,
    TomamichelEtAlEve,
)
from src.reconciliation import CascadeProtocol
from src.execution import (
    execute_run_and_store,
    execute_reconciliation_and_store,
)

from src.data_management import (
    check_if_folder_is_correct,
    setup_folder,
    save_db_in_folder,
    load_db_from_folder,
    DataBase,
    RunCols,
)


def get_db(folder_path: Path) -> DataBase:
    """
    Gets the data base from the folder and loads in the environments and
    protocols. If the folder is unexistent and/or not setup correctly, it wil
    be created and setup correctly.

    :param folder_path: The path to the folder the database should contain
    :type folder_path: Path
    :return: The database
    :rtype: DataBase
    """

    if not check_if_folder_is_correct(folder_path):
        setup_folder(folder_path)
    db = load_db_from_folder(folder_path)

    dist_prots = [BB84KeyDistribution, TomamichelEtAlKeyDistribution]
    db.load_distribution_protocols(dist_prots)

    envs = [
        NoiselessEnvironment,
        SingleQbitAmplitudeDamping,
        SingleQbitDepolarization,
        BB84Eve,
        TomamichelEtAlEve,
    ]
    db.load_environments(envs)

    rec_prots = [CascadeProtocol]
    db.load_reconciliation_protocols(rec_prots)

    amp_prots = []
    db.load_amplification_protocols(amp_prots)

    return db


def print_run_info(
    prot: type[DistributionProtocol],
    env: type[Environment],
    **params,
):
    """Prints the information about a run to see progress"""
    print(
        f"Started simulation of protocol {prot.get_name()} with environment"
        + f"{env.get_name()}.\nParams : "
    )
    for name, val in params.items():
        print(f"param name : {name}\t\t value : {val}")


TARGETED_KEY_LENGTHS = [2_000, 4_000, 6_000, 8_000, 10_000]
NUM_REPETITIONS = 30
ENV_PROBS = [0.2, 0.4, 0.6, 0.8, 1.0]


def simulate_BB84_no_noise(
    rng: np.random.Generator,
    db: DataBase,
    folder_path: Path,
) -> None:
    """Simulates BB84 QKD with no noise"""
    env = NoiselessEnvironment()
    for key_length in TARGETED_KEY_LENGTHS:
        seeds = rng.integers(2**32, size=NUM_REPETITIONS)

        print_run_info(
            BB84KeyDistribution,
            NoiselessEnvironment,
            key_length=key_length,
        )

        for seed in seeds:
            prot = BB84KeyDistribution(1.0, key_length, seed)
            execute_run_and_store(prot, env, db)

        save_db_in_folder(db, folder_path)


def simulate_BB84_with_Eve(
    rng: np.random.Generator,
    db: DataBase,
    folder_path: Path,
):
    """Simulates the BB84 with it's own Eve"""
    for eve_attack_prob in ENV_PROBS:
        for key_length in TARGETED_KEY_LENGTHS:
            seeds = rng.integers(2**32, size=NUM_REPETITIONS)

            print_run_info(
                BB84KeyDistribution,
                BB84Eve,
                eve_attack_probability=eve_attack_prob,
                key_length=key_length,
            )

            for seed in seeds:
                eve = BB84Eve(eve_attack_prob, seed)
                prot = BB84KeyDistribution(1.0, key_length, seed)
                execute_run_and_store(prot, eve, db)

            save_db_in_folder(db, folder_path)


def simulate_BB84_with_amplitude_damping(
    rng: np.random.Generator, db: DataBase, folder_path: Path
):
    """Simulates the BB84 with single qbit amplitude damping"""
    for prob in ENV_PROBS:
        env = SingleQbitAmplitudeDamping(prob)
        for key_length in TARGETED_KEY_LENGTHS:
            seeds = rng.integers(2**32, size=NUM_REPETITIONS)

            print_run_info(
                BB84KeyDistribution,
                SingleQbitAmplitudeDamping,
                env_prob=prob,
                key_length=key_length,
            )

            for seed in seeds:
                prot = BB84KeyDistribution(1.0, key_length, seed)
                execute_run_and_store(prot, env, db)

            save_db_in_folder(db, folder_path)


def simulate_BB84_with_depolarization(
    rng: np.random.Generator, db: DataBase, folder_path: Path
):
    """Simulates the BB84 with single qbit depolarization"""
    for prob in ENV_PROBS:
        env = SingleQbitDepolarization(prob)
        for key_length in TARGETED_KEY_LENGTHS:
            seeds = rng.integers(2**32, size=NUM_REPETITIONS)

            print_run_info(
                BB84KeyDistribution,
                SingleQbitDepolarization,
                env_prob=prob,
                key_length=key_length,
            )

            for seed in seeds:
                prot = BB84KeyDistribution(1.0, key_length, seed)
                execute_run_and_store(prot, env, db)

            save_db_in_folder(db, folder_path)


def simulate_Tomamichel_no_noise(
    rng: np.random.Generator,
    db: DataBase,
    folder_path: Path,
) -> None:
    """Simulates Tomamichel et al. QKD with no noise"""
    env = NoiselessEnvironment()
    for bloc_size in TARGETED_KEY_LENGTHS:
        detection_size = bloc_size // 4
        seeds = rng.integers(2**32, size=NUM_REPETITIONS)

        print_run_info(
            TomamichelEtAlKeyDistribution,
            NoiselessEnvironment,
            bloc_size=bloc_size,
            detection_size=detection_size,
        )

        for seed in seeds:
            prot = TomamichelEtAlKeyDistribution(
                bloc_size, detection_size, 1.0, seed
            )
            execute_run_and_store(prot, env, db)

        save_db_in_folder(db, folder_path)


def simulate_Tomamichel_with_Eve(
    rng: np.random.Generator,
    db: DataBase,
    folder_path: Path,
):
    """Simulates the Tomamichel et al. with it's own Eve"""
    for eve_attack_prob in ENV_PROBS:
        for bloc_size in TARGETED_KEY_LENGTHS:
            detection_size = bloc_size // 4
            seeds = rng.integers(2**32, size=NUM_REPETITIONS)

            print_run_info(
                TomamichelEtAlKeyDistribution,
                TomamichelEtAlEve,
                eve_attack_probability=eve_attack_prob,
                bloc_size=bloc_size,
                detection_size=detection_size,
            )

            for seed in seeds:
                eve = TomamichelEtAlEve(
                    eve_attack_prob,
                    seed,
                    bloc_size,
                    detection_size,
                )
                prot = TomamichelEtAlKeyDistribution(
                    bloc_size,
                    detection_size,
                    1.0,
                    seed,
                )
                execute_run_and_store(prot, eve, db)

            save_db_in_folder(db, folder_path)


def simulate_Tomamichel_with_amplitude_damping(
    rng: np.random.Generator, db: DataBase, folder_path: Path
):
    """Simulates the Tomamichel et al. with single qbit amplitude damping"""
    for prob in ENV_PROBS:
        env = SingleQbitAmplitudeDamping(prob)
        for bloc_size in TARGETED_KEY_LENGTHS:
            detection_size = bloc_size // 4
            seeds = rng.integers(2**32, size=NUM_REPETITIONS)

            print_run_info(
                TomamichelEtAlKeyDistribution,
                SingleQbitAmplitudeDamping,
                env_prob=prob,
                bloc_size=bloc_size,
                detection_size=detection_size,
            )

            for seed in seeds:
                prot = TomamichelEtAlKeyDistribution(
                    bloc_size,
                    detection_size,
                    1.0,
                    seed,
                )
                execute_run_and_store(prot, env, db)

            save_db_in_folder(db, folder_path)


def simulate_Tomamichel_with_depolarization(
    rng: np.random.Generator,
    db: DataBase,
    folder_path: Path,
):
    """Simulates the Tomamichel et al. with single qbit depolarization"""
    for prob in ENV_PROBS:
        env = SingleQbitDepolarization(prob)
        for bloc_size in TARGETED_KEY_LENGTHS:
            detection_size = bloc_size // 4
            seeds = rng.integers(2**32, size=NUM_REPETITIONS)

            print_run_info(
                TomamichelEtAlKeyDistribution,
                SingleQbitDepolarization,
                env_prob=prob,
                bloc_size=bloc_size,
                detection_size=detection_size,
            )

            for seed in seeds:
                prot = TomamichelEtAlKeyDistribution(
                    bloc_size,
                    detection_size,
                    1.0,
                    seed,
                )
                execute_run_and_store(prot, env, db)

            save_db_in_folder(db, folder_path)


def main():
    """Main function"""
    folder_path = Path.cwd() / "results"

    db = get_db(folder_path)
    rng = np.random.default_rng()

    # simulate_BB84_no_noise(rng, db, folder_path)
    # simulate_Tomamichel_no_noise(rng, db, folder_path)

    # simulate_BB84_with_Eve(rng, db, folder_path)
    # simulate_Tomamichel_with_Eve(rng, db, folder_path)

    # simulate_BB84_with_amplitude_damping(rng, db, folder_path)
    # simulate_Tomamichel_with_amplitude_damping(rng, db, folder_path)

    # simulate_BB84_with_depolarization(rng, db, folder_path)
    # simulate_Tomamichel_with_depolarization(rng, db, folder_path)

    BATCH_SIZE = 100
    delta = 0

    for run_id in db.run[RunCols.ID]:
        execute_reconciliation_and_store(
            db,
            CascadeProtocol(rng.integers(0, 2**32 - 1, 1)[0], 10, 0.8, 5, 3),
            run_id,
        )

        delta += 1
        if delta >= BATCH_SIZE:
            save_db_in_folder(db, folder_path)
            delta = 0

    save_db_in_folder(db, folder_path)


if __name__ == "__main__":
    main()
