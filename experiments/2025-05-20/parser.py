from lab.parser import Parser
import re


def add_coverage(content, props):
    props["coverage"] = 0

    if "Total time:" in content:
        assert "fasb" in content or "Number of plans:" in content
        props["coverage"] = 1

    if "Planalyst time" in content:
        assert "fasb" in content or "Number of plans:" in content
        props["coverage"] = 1


def add_fasb_num_plans(content, props):
    if "Running fasb" not in content:
        return

    if "Terminating fasb." not in content:
        return

    match = re.search(r"#\!\n(\d+)\n", content)
    if match:
        props["num_plans"] = int(match.group(1))


class CustomParser(Parser):
    def __init__(self):
        Parser.__init__(self)


def get_parser():
    parser = CustomParser()
    parser.add_pattern("num_plans", r"Number of plans: (.+)", type=int)
    parser.add_pattern("total_time", r"Total time: (.+)s", type=float)
    parser.add_pattern("total_time", r"Planalyst time: (.+)s", type=float)
    parser.add_function(add_coverage)
    parser.add_function(add_fasb_num_plans)
    return parser
