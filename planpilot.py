#! /usr/bin/env python3
import logging
import os
import re
import select
import shutil
import sys
import utils

from collections import OrderedDict
from subprocess import Popen, PIPE

from time import sleep

logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format="[%(asctime)s] %(levelname)s ::: %(message)s",
)
logger = logging.getLogger(__name__)


def run_plasp(domain, instance, lp, encoding, dump_output, pddl_instance=True):
    binary_path = "./bin/plasp"
    command = [binary_path, "translate", instance] # SAS+ instance
    if pddl_instance:
        command = [binary_path, "translate", domain, instance]

    with open(lp, "w") as lp_file:
        # First, we add the corresponding sequential encoding to it
        encoding = "encodings/exact-sequential-horizon.lp"
        if args.encoding == 'bounded':
            encoding = "encodings/bounded-sequential-horizon.lp"
        with open(encoding) as seq_encoding:
            lp_file.write(seq_encoding.read())

        time_steps_encoding = "encodings/action-per-time-step.lp"
        if args.abstract_time_steps:
            time_steps_encoding = "encodings/abstract-time-steps.lp"

        with open(time_steps_encoding) as time_encoding:
            lp_file.write(time_encoding.read())

        # Now, we run plasp to produce the instance-specific info
        process = Popen(command, stdout=lp_file, stdin=PIPE, stderr=PIPE, text=True)

    time = utils.get_elapsed_time()
    _, error = process.communicate()
    logging.info(f"plasp time: {utils.get_elapsed_time() - time:.2f}s")

    logger.info(f"plasp return code: {process.returncode}")
    if process.returncode != 0:
        print(error)
        exit(process.returncode)


def run_fasb(lp, horizon):
    binary_path = "./bin/fasb-x86_64-unknown-linux-gnu/fasb"
    command = [binary_path, lp, "-c", f"horizon={horizon}", "0"]

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

    logger.info("Running fasb with script script.fsb...")
    run_fasb(
        args.lp_name,
        args.horizon)

    if args.cleanup:
        remove_lp_files()

    logging.info(f"Total time: {utils.get_elapsed_time():.2f}s")
    logger.info("Done!")
