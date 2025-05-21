import os
from pathlib import Path
import platform
import re
import parser

from downward.experiment import FastDownwardExperiment, Experiment
from downward.reports.scatter import ScatterPlotReport
from downward.reports.taskwise import TaskwiseReport
from lab.reports import Attribute
from lab.environments import (
    BaselSlurmEnvironment,
    LocalEnvironment,
    TetralithEnvironment,
)

# Silence import-unused messages. Experiment scripts may use these imports.
assert (
    BaselSlurmEnvironment
    and FastDownwardExperiment
    and Experiment
    and LocalEnvironment
    and ScatterPlotReport
    and TaskwiseReport
    and TetralithEnvironment
)

PLANPILOT_BENCHMARKS_DIR = os.environ["PLANPILOT_BENCHMARKS"]
IPC_BENCHMARKS_DIR = os.environ["DOWNWARD_BENCHMARKS"]

REMOTE_BINDS = [
    (os.environ["HOME"], os.environ["HOME"]),
    ("/proj/parground/planpilot/", "/proj/parground/planpilot/"),
]

# Singularity Planners
PLANNER_IMAGE_PATH = os.environ["PLANNER_IMAGES"]
SIF_PLANPILOT = os.path.join(PLANNER_IMAGE_PATH, "planpilot.sif")
SIF_PLANALYST = os.path.join(PLANNER_IMAGE_PATH, "planalyst.sif")
SIF_SYMK = os.path.join(PLANNER_IMAGE_PATH, "symk.sif")
SIF_KSTAR = os.path.join(PLANNER_IMAGE_PATH, "kstar.sif")


DIR = Path(__file__).resolve().parent
NODE = platform.node()
# Cover both the Basel and Linköping clusters for simplicity.
REMOTE = NODE.endswith((".scicore.unibas.ch", ".cluster.bc2.ch")) or re.match(
    r"tetralith\d+\.nsc\.liu\.se|n\d+", NODE
)


def get_bind_cmd():
    cmd = ["singularity", "run"]
    if REMOTE:
        for fr, to in REMOTE_BINDS:
            cmd += ["--bind", f"{fr}:{to}"]
    return cmd


def get_cmd_with_timeout(cmd, timeout_in_sec):
    return ["timeout", str(timeout_in_sec)] + cmd[:]


SUITE = [
    "airport",
    "barman-opt14-strips",
    "blocks",
    "childsnack-opt14-strips",
    "depot",
    "driverlog",
    "freecell",
    "grid",
    "gripper",
    "hiking-opt14-strips",
    "logistics00",
    "logistics98",
    "miconic",
    "movie",
    "mprime",
    "mystery",
    "nomystery-opt11-strips",
    "organic-synthesis-opt18-strips",
    "parking-opt11-strips",
    "parking-opt14-strips",
    "pipesworld-notankage",
    "pipesworld-tankage",
    "psr-small",
    "quantum-layout-opt23-strips",
    "rovers",
    "satellite",
    "snake-opt18-strips",
    "storage",
    "termes-opt18-strips",
    "tidybot-opt11-strips",
    "tidybot-opt14-strips",
    "tpp",
    "visitall-opt11-strips",
    "visitall-opt14-strips",
    "zenotravel",
]

DOMAIN_GROUPS = {
    "airport": ["airport"],
    "barman": ["barman-opt14-strips"],
    "blocks": ["blocks"],
    "childsnack": ["childsnack-opt14-strips"],
    "depot": ["depot"],
    "driverlog": ["driverlog"],
    "freecell": ["freecell"],
    "grid": ["grid"],
    "gripper": ["gripper"],
    "hiking": ["hiking-opt14-strips"],
    "logistics": ["logistics00", "logistics98"],
    "miconic": ["miconic"],
    "movie": ["movie"],
    "mprime": ["mprime"],
    "mystery": ["mystery"],
    "nomystery": ["nomystery-opt11-strips"],
    "organic-synthesis": ["organic-synthesis-opt18-strips"],
    "parking": ["parking-opt11-strips", "parking-opt14-strips"],
    "pipesworld-nt": ["pipesworld-notankage"],
    "pipesworld-t": ["pipesworld-tankage"],
    "psr-small": ["psr-small"],
    "quantum-layout": ["quantum-layout-opt23-strips"],
    "rovers": ["rovers"],
    "satellite": ["satellite"],
    "snake": ["snake-opt18-strips"],
    "storage": ["storage"],
    "termes": ["termes-opt18-strips"],
    "tidybot": ["tidybot-opt11-strips", "tidybot-opt14-strips"],
    "tpp": ["tpp"],
    "visitall": ["visitall-opt11-strips", "visitall-opt14-strips"],
    "zenotravel": ["zenotravel"],
}


assert len(SUITE) == sum([len(DOMAIN_GROUPS[key]) for key in DOMAIN_GROUPS])

DOMAIN_RENAMINGS = {}
for group_name, domains in DOMAIN_GROUPS.items():
    for domain in domains:
        DOMAIN_RENAMINGS[domain] = group_name
for group_name in DOMAIN_GROUPS:
    DOMAIN_RENAMINGS[group_name] = group_name


def group_domains(run):
    old_domain = run["domain"]
    run["domain"] = DOMAIN_RENAMINGS[old_domain]
    run["problem"] = old_domain + "-" + run["problem"]
    run["id"][2] = run["problem"]
    return run


def domain_as_category(run1, run2):
    # run2['domain'] has the same value, because we always
    # compare two runs of the same problem.
    return run1["domain"]
