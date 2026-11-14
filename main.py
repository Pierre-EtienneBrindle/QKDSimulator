from pathlib import Path
import numpy as np

from src.distribution import (
    BB84KeyDistribution,
    TomamichelEtAlKeyDistribution,
    NoiselessEnvironment,
    SingleQbitAmplitudeDamping,
    SingleQbitDepolarization,
)
from src.execution import execute_run_and_store

from src.data_management import (
    DataBase,
    save_db_in_folder,
    load_db_from_folder,
)


def main():
    print("WELCOME TO QKD SIMULATOR")

    folder_path = Path.cwd() / "results"
    if not folder_path.exists():
        save_db_in_folder(DataBase(), folder_path)
    db = load_db_from_folder(folder_path)

    protocols = [BB84KeyDistribution, TomamichelEtAlKeyDistribution]
    db.load_distribution_protocols(protocols)

    envs = [
        NoiselessEnvironment,
        SingleQbitAmplitudeDamping,
        SingleQbitDepolarization,
    ]
    db.load_environments(envs)

    rng = np.random.default_rng()
    num_errors = 4
    max_errors = [
        0.1 + 0.4 * error / num_errors for error in range(num_errors + 1)
    ]

    error_probabilities = [i / 10 for i in range(6)]

    num_repetitions = 150

    BB84_target_key_size = 150

    Tomamichel_bloc_len = 150
    Tomamichel_detection_len = 50

    # BB84 Noiseless
    env = NoiselessEnvironment()
    for max_error_rate in max_errors:
        seeds = rng.integers(2**32 - 1, size=num_repetitions)
        for seed in seeds:
            protocol = BB84KeyDistribution(
                max_error_rate,
                BB84_target_key_size,
                seed,
            )
            execute_run_and_store(protocol, env, db)
        save_db_in_folder(db, folder_path)

    # BB84 Amplitude damping
    for p in error_probabilities:
        env = SingleQbitAmplitudeDamping(p)
        for max_error_rate in max_errors:
            seeds = rng.integers(2**32 - 1, size=num_repetitions)
            for seed in seeds:
                protocol = BB84KeyDistribution(
                    max_error_rate,
                    BB84_target_key_size,
                    seed,
                )
                execute_run_and_store(protocol, env, db)
            save_db_in_folder(db, folder_path)

    # BB84 Depolarizing
    for p in error_probabilities:
        env = SingleQbitDepolarization(p)
        for max_error_rate in max_errors:
            seeds = rng.integers(2**32 - 1, size=num_repetitions)
            for seed in seeds:
                protocol = BB84KeyDistribution(
                    max_error_rate,
                    BB84_target_key_size,
                    seed,
                )
                execute_run_and_store(protocol, env, db)
            save_db_in_folder(db, folder_path)

    # Tomamichel Noiseless
    env = NoiselessEnvironment()
    for max_error_rate in max_errors:
        seeds = rng.integers(2**32 - 1, size=num_repetitions)
        for seed in seeds:
            protocol = TomamichelEtAlKeyDistribution(
                Tomamichel_bloc_len,
                Tomamichel_detection_len,
                max_error_rate,
                seed,
            )
            execute_run_and_store(protocol, env, db)
        save_db_in_folder(db, folder_path)

    # Tomamichel Amplitude damping
    for p in error_probabilities:
        env = SingleQbitAmplitudeDamping(p)
        for max_error_rate in max_errors:
            seeds = rng.integers(2**32 - 1, size=num_repetitions)
            for seed in seeds:
                protocol = TomamichelEtAlKeyDistribution(
                    Tomamichel_bloc_len,
                    Tomamichel_detection_len,
                    max_error_rate,
                    seed,
                )
                execute_run_and_store(protocol, env, db)
            save_db_in_folder(db, folder_path)

    # BB84 Depolarizing
    for p in error_probabilities:
        env = SingleQbitDepolarization(p)
        for max_error_rate in max_errors:
                seeds = rng.integers(2**32 - 1, size=num_repetitions)
                for seed in seeds:
                    protocol = TomamichelEtAlKeyDistribution(
                        Tomamichel_bloc_len,
                        Tomamichel_detection_len,
                        max_error_rate,
                        seed,
                    )
                    execute_run_and_store(protocol, env, db)
                save_db_in_folder(db, folder_path)


if __name__ == "__main__":
    main()
