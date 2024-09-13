#! /usr/bin/env python3
import logging
import os
import re
import shutil
import sys
import utils

from collections import OrderedDict
from subprocess import Popen, PIPE


logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format="[%(asctime)s] %(levelname)s ::: %(message)s",
)
logger = logging.getLogger(__name__)


def run_plasp(domain, instance, lp, encoding, dump_output):
    binary_path = "./bin/plasp"
    command = [binary_path, "translate", domain, instance]

    with open(lp, "w") as lp_file:
        # First, we add the corresponding sequential encoding to it
        encoding = "encodings/exact-sequential-horizon.lp"
        if args.encoding == 'bounded':
            encoding = "encodings/bounded-sequential-horizon.lp"
        with open(encoding) as seq_encoding:
            lp_file.write(seq_encoding.read())

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
    binary_path = "./bin/fasb"
    command = [binary_path, lp, "-c", f"horizon={horizon}", "0", "script.fsb"]

    process = Popen(command, stdout=PIPE, stdin=PIPE, stderr=PIPE, text=True)

    time = utils.get_elapsed_time()
    output, error = process.communicate()

    if process.returncode != 0:
        print(error)
        exit(process.returncode)

    logging.info("fasb output:")
    print(output)

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
    if not os.path.isfile(domain_file):
        sys.stderr.write("Error: Domain file does not exist.\n")
        sys.exit()
    if not os.path.isfile(instance_file):
        sys.stderr.write("Error: Instance file does not exist.\n")
        sys.exit()

    logger.info("Running plasp...")
    run_plasp(
        args.domain,
        args.instance,
        args.lp_name,
        args.encoding,
        args.dump_output)

    logger.info("Running fasb with script script.fsb...")
    run_fasb(
        args.lp_name,
        args.horizon)

    if args.cleanup:
        remove_lp_files()

    logging.info(f"Total time: {utils.get_elapsed_time():.2f}s")
    logger.info("Done!")
