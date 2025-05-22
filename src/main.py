from naive_runner import NaiveRunner
import time

def main ():
    start_time = time.time()
    NaiveRunner.execute_naive_all_pairs_matching()
    print(f"Naive approach completed in {time.time() - start_time:.2f} seconds")

    # TODO: Uncomment this when implementation is ready to execute from command line
    # Ensure no extra args are passed
    # if len(sys.argv) != 2:
    #     print("Error: Exactly one argument required: 'naive' or 'group'.")
    #     sys.exit(1)

    # TODO: Uncomment this when implementation is ready to execute from command line
    # In case a user execute main file with --help flag
    # parser = argparse.ArgumentParser(description="Run Spark job with 'naive' or 'group' argument")
    # parser.add_argument("mode", nargs=1, help="Execution mode: naive or group Map Reduce implementation")
    #
    # args = parser.parse_args()
    #
    # if args.mode[0] == "naive":
    #     naive_runner = NaiveRunner()
    #     naive_runner.run()
    # elif args.mode[0] == "group":
    #     group_runner = GroupRunner()
    #     group_runner.run()
    # else:
    #     print(f"Error: Invalid argument '{args.mode[0]}'. Use 'naive' or 'group'.")
    #     sys.exit(1)

if __name__ == "__main__":
    main()

