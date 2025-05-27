import argparse
import time
import sys

from naive_runner import NaiveRunner
from group_runner import GroupRunner


def main():
    # In case a user execute main file with --help flag
    parser = argparse.ArgumentParser(
        description="Run Spark job with 'naive' or 'group' argument and 'small', 'medium' or 'large' for dataset")
    parser.add_argument("mode", help="Execution mode: naive or group of Map Reduce implementation")
    parser.add_argument("dataset_size", help="Dataset size: small, medium, or large")

    args = parser.parse_args()
    start_time = time.time()

    valid_dataset_sizes = {"small", "medium", "large"}

    if args.mode == "naive" and args.dataset_size in valid_dataset_sizes:
        NaiveRunner.execute_naive_all_pairs_matching(args.dataset_size)
        print(f"Naive approach completed in {time.time() - start_time:.2f} seconds", flush=True)
    elif args.mode == "group" and args.dataset_size in valid_dataset_sizes:
        GroupRunner().execute_group_all_pairs_matching(args.dataset_size)
        print(f"Group approach completed in {time.time() - start_time:.2f} seconds", flush=True)
    else:
        print(f"Error: Invalid mode argument or dataset argument. Run with --help flag to get help information!",
              flush=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
