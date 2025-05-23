import argparse
import time
import sys

from naive_runner import NaiveRunner
from group_runner import GroupRunner

def main ():

    if len(sys.argv) != 2:  # Ensure no extra args are passed
        print("Error: Exactly one argument required: 'naive' or 'group'.")
        sys.exit(1)

    # In case a user execute main file with --help flag
    parser = argparse.ArgumentParser(description="Run Spark job with 'naive' or 'group' argument")
    parser.add_argument("mode", nargs=1, help="Execution mode: naive or group of Map Reduce implementation")

    args = parser.parse_args()
    start_time = time.time()

    if args.mode[0] == "naive":
        NaiveRunner.execute_naive_all_pairs_matching()
        print(f"Naive approach completed in {time.time() - start_time:.2f} seconds")
    elif args.mode[0] == "group":
        GroupRunner().execute_group_all_pairs_matching()
        print(f"Group approach completed in {time.time() - start_time:.2f} seconds")
    else:
        print(f"Error: Invalid argument '{args.mode[0]}'. Use 'naive' or 'group'.")
        sys.exit(1)

if __name__ == "__main__":
    main()

