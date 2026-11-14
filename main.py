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
    save_db_in_folder,
    load_db_from_folder,
)


def main():
    print("WELCOME TO QKD SIMULATOR")

    folder_path = Path.cwd() / "results"
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

    num_repetitions = 100

    BB84_num_target_key_size = 5
    BB84_delta_target_key_size = 50
    BB84_target_key_sizes = [
        100 + i * BB84_delta_target_key_size
        for i in range(BB84_num_target_key_size + 1)
    ]

    Tomamichel_num_bloc_len = 5
    Tomamichel_delta_bloc_len = 50
    Tomamichel_bloc_lens = [
        100 + i * Tomamichel_delta_bloc_len
        for i in range(Tomamichel_num_bloc_len + 1)
    ]
    Tomamichel_num_detection_len = 5
    Tomamichel_delta_detection_len = 50
    Tomamichel_detection_lens = [
        100 + i * Tomamichel_delta_detection_len
        for i in range(Tomamichel_num_detection_len + 1)
    ]

    # BB84 Noiseless
    env = NoiselessEnvironment()
    for max_error_rate in max_errors:
        for target_key_size in BB84_target_key_sizes:
            seeds = rng.integers(2**32 - 1, size=num_repetitions)
            for seed in seeds:
                protocol = BB84KeyDistribution(
                    max_error_rate,
                    target_key_size,
                    seed,
                )
                execute_run_and_store(protocol, env, db)
            save_db_in_folder(db, folder_path)

    # BB84 Amplitude damping
    for p in error_probabilities:
        env = SingleQbitAmplitudeDamping(p)
        for max_error_rate in max_errors:
            for target_key_size in BB84_target_key_sizes:
                seeds = rng.integers(2**32 - 1, size=num_repetitions)
                for seed in seeds:
                    protocol = BB84KeyDistribution(
                        max_error_rate,
                        target_key_size,
                        seed,
                    )
                    execute_run_and_store(protocol, env, db)
                save_db_in_folder(db, folder_path)

    # BB84 Depolarizing
    for p in error_probabilities:
        env = SingleQbitDepolarization(p)
        for max_error_rate in max_errors:
            for target_key_size in BB84_target_key_sizes:
                seeds = rng.integers(2**32 - 1, size=num_repetitions)
                for seed in seeds:
                    protocol = BB84KeyDistribution(
                        max_error_rate,
                        target_key_size,
                        seed,
                    )
                    execute_run_and_store(protocol, env, db)
                save_db_in_folder(db, folder_path)

    # Tomamichel Noiseless
    env = NoiselessEnvironment()
    for max_error_rate in max_errors:
        for bloc_len in Tomamichel_bloc_lens:
            for detection_len in Tomamichel_detection_lens:
                seeds = rng.integers(2**32 - 1, size=num_repetitions)
                for seed in seeds:
                    protocol = TomamichelEtAlKeyDistribution(
                        bloc_len,
                        detection_len,
                        max_error_rate,
                        seed,
                    )
                    execute_run_and_store(protocol, env, db)
                save_db_in_folder(db, folder_path)

    # Tomamichel Amplitude damping
    for p in error_probabilities:
        env = SingleQbitAmplitudeDamping(p)
        for max_error_rate in max_errors:
            for bloc_len in Tomamichel_bloc_lens:
                for detection_len in Tomamichel_detection_lens:
                    seeds = rng.integers(2**32 - 1, size=num_repetitions)
                    for seed in seeds:
                        protocol = TomamichelEtAlKeyDistribution(
                            bloc_len,
                            detection_len,
                            max_error_rate,
                            seed,
                        )
                        execute_run_and_store(protocol, env, db)
                    save_db_in_folder(db, folder_path)

    # BB84 Depolarizing
    for p in error_probabilities:
        env = SingleQbitDepolarization(p)
        for max_error_rate in max_errors:
            for bloc_len in Tomamichel_bloc_lens:
                for detection_len in Tomamichel_detection_lens:
                    seeds = rng.integers(2**32 - 1, size=num_repetitions)
                    for seed in seeds:
                        protocol = TomamichelEtAlKeyDistribution(
                            bloc_len,
                            detection_len,
                            max_error_rate,
                            seed,
                        )
                        execute_run_and_store(protocol, env, db)
                    save_db_in_folder(db, folder_path)


if __name__ == "__main__":
    main()
