#! /usr/bin/env python3
import logging
import os
import select
import sys
import utils

from subprocess import Popen, PIPE


logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format="[%(asctime)s] %(levelname)s ::: %(message)s",
)
logger = logging.getLogger(__name__)

dirname = os.path.dirname(__file__)

def fix_path(path):
    return os.path.join(dirname, path)

# TODO: implement dump_out
def run_plasp(domain, instance, lp, encoding, dump_output, pddl_instance=True):
    binary_path = fix_path("bin/plasp")
    command = [binary_path, "translate", instance] # SAS+ instance
    if pddl_instance:
        command = [binary_path, "translate", domain, instance]

    with open(lp, "w") as lp_file:
        # First, we add the corresponding sequential encoding to it
        encoding = fix_path("encodings/exact-sequential-horizon.lp")
        if args.encoding == 'bounded':
            encoding = fix_path("encodings/bounded-sequential-horizon.lp")
        with open(encoding) as seq_encoding:
            lp_file.write(seq_encoding.read())

        time_steps_encoding = fix_path("encodings/action-per-time-step.lp")
        if args.abstract_time_steps:
            time_steps_encoding = fix_path("encodings/abstract-time-steps.lp")

        with open(time_steps_encoding) as time_encoding:
            lp_file.write(time_encoding.read())

        if args.partial_plan:
            logger.info(f"Using partial plan '{args.partial_plan}'...")
            constraints: str | None = translate_partial_plan_into_constraints(args.partial_plan)
            lp_file.write("\n%%%%%%% partial plan encoding\n" + constraints + "\n")

        # Now, we run plasp to produce the instance-specific info
        process = Popen(command, stdout=lp_file, stdin=PIPE, stderr=PIPE, text=True)

    time = utils.get_elapsed_time()
    _, error = process.communicate()
    logging.info(f"plasp time: {utils.get_elapsed_time() - time:.2f}s")

    logger.info(f"plasp return code: {process.returncode}")
    if process.returncode != 0:
        print(error)
        exit(process.returncode)


def run_fasb(lp, horizon, script=None):
    binary_path = fix_path("bin/fasb-x86_64-unknown-linux-gnu/fasb") # TODO don't keep multiple versions

    if script:
        binary_path = fix_path("bin/fasb_interpreter")
        logger.info(f"Executing fasb script {script}...")

    command = [binary_path, lp, "-c", f"horizon={horizon}", "0"]

    if script:
        full_script_path = fix_path(script)
        command.append(full_script_path)

    if args.dry:
        logging.info("Dry startup...")
        logging.info("To compute facets matching some regular expression 're', use the command '!? re'...")
        command.append("--f")

    # TODO Probably must be different if we want to use script version
    process = Popen(command, stdout=PIPE, stdin=PIPE, stderr=PIPE,
                    text=True, universal_newlines=True, bufsize=1)

    time = utils.get_elapsed_time()

    logging.info("Starting fasb... To quit the interactive mode, use the command ':q'.")

    # Set up the file descriptors for select
    input_stream = sys.stdin
    output_stream = process.stdout
    error_stream = process.stderr

    prompts = 0
    try:
        terminated = False
        while not terminated:
            # Use select to wait for input/output readiness
            reads, _, _ = select.select([input_stream, output_stream, error_stream], [], [])
            for stream in reads:
                if stream == output_stream:
                    # Read from the subprocess's output
                    output = process.stdout.readline()
                    if output:  # If there's output, print it
                        print(output.strip())
                    else:
                        # If no output, the process might have closed
                        logging.info("Terminating fasb.")
                        logging.info(f"Number of prompts: {prompts}")
                        terminated = True
                        break

                elif stream == input_stream:
                    # Get user input
                    user_input = input()
                    # Send input to the subprocess
                    process.stdin.write(user_input + '\n')
                    process.stdin.flush()  # Ensure it's sent immediately
                    prompts = prompts + 1

                elif stream == error_stream:
                    # Read from the subprocess's error stream if needed
                    error_output = process.stderr.readline()
                    if error_output:
                        print("Error:", error_output.strip())
                        terminated = True

    except KeyboardInterrupt:
        # Handle Ctrl+C to exit cleanly
        print("Exiting...")
        process.stdin.write('exit()\n')  # Send exit command to the subprocess
        process.stdin.flush()

    logging.info(f"fasb time: {utils.get_elapsed_time() - time:.2f}s")

    logger.info(f"fasb return code: {process.returncode}")


def remove_lp_files():
    current_directory = os.getcwd()

    for file_name in os.listdir(current_directory):
        file_path = os.path.join(current_directory, file_name)
        if os.path.isfile(file_path) and file_name.endswith(".lp"):
            try:
                os.remove(file_path)
            except Exception as e:
                logger.error(f"Error removing {file_path}: {e}")


def translate_partial_plan_into_constraints(file_path: str) -> str | None:
    # TODO: give the name of specific format
    """
    Expects actions in specific format.

    Example:
    `a b c (1) d e (1)`
    will be translated into
    `
    :- not occurs(action(("a","b","c")),1).
    :- not occurs(action(("d","e")),2).
    `
    """
    global PARTIAL_PLAN_DELIMITER
    PARTIAL_PLAN_DELIMITER = "(1)"

    try:
        with open(file_path, "r") as f:
            actions = filter(
                lambda x: x,
                map(lambda x: x.strip(), f.read().split(PARTIAL_PLAN_DELIMITER)),
            )
            return "\n".join(
                map(
                    lambda t: translate_action_to_constraint(*t[::-1]),
                    enumerate(actions),
                )
            )
    except Exception as e:
        logger.error(f"could not read partial plan '{file_path}': {e}")


def translate_action_to_constraint(action: str, at: int) -> str:
    """
    Translates whitespace-separated action into integrity constraint.

    Example:
    `a b c` as first action will be translated into
    `:- not occurs(action(("a","b","c")),1).`
    """
    return (
        ":- not occurs(action(("
        + ",".join(map(lambda x: f'"{x}"', action.split(" ")))
        + f")),{at+1})."
    )





if __name__ == "__main__":
    args = utils.parse_arguments()

    domain_file = args.domain
    instance_file = args.instance
    if args.is_pddl_instance and not os.path.isfile(domain_file):
        sys.stderr.write("Error: Domain file does not exist.\n")
        sys.exit()
    if not os.path.isfile(instance_file):
        sys.stderr.write("Error: Instance file does not exist.\n")
        sys.exit()

    logger.info("Running plasp...")
    if args.is_pddl_instance:
        run_plasp(
            args.domain,
            args.instance,
            args.lp_name,
            args.encoding,
            args.dump_output)
    else:
        run_plasp(
            "",
            args.instance,
            args.lp_name,
            args.encoding,
            args.dump_output,
            False)

    logger.info("Running fasb...")
    run_fasb(
        args.lp_name,
        args.horizon,
        args.script)

    if args.cleanup:
        remove_lp_files()

    logging.info(f"Total time: {utils.get_elapsed_time():.2f}s")
    logger.info("Done!")
