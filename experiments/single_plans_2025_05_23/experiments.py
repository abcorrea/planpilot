#! /usr/bin/env python3

import parser
import project

from cactus_plot import CactusPlot
from check_relative import OptimalityFilter
from downward.reports.absolute import AbsoluteReport
from downward import suites


def add_resources(run, instance):
    run.add_resource("domain", instance.domain_file, symlink=True)
    run.add_resource("problem", instance.problem_file, symlink=True)


def set_properties(run, instance, config_name, config, config_driver_options):
    run.set_property("domain", instance.domain)
    run.set_property("problem", instance.problem)
    run.set_property("algorithm", config_name)
    run.set_property("component_options", config)
    run.set_property("driver_options", config_driver_options)
    run.set_property("id", [config_name, instance.domain, instance.problem])


MEMORY_LIMIT = 3584  # 3GiB
MEMORY_PADDING = 3872 - MEMORY_LIMIT  # TetralithEnvironment has 3872 MB per cpu
TIME_LIMIT = 30 * 60
DRIVER_OPTIONS = [
    "--overall-time-limit",
    f"{TIME_LIMIT}s",
    "--overall-memory-limit",
    f"{MEMORY_LIMIT}M",
]

BENCHMARK_DIR = project.PLANPILOT_BENCHMARKS_DIR

if project.REMOTE:
    SUITE = ["beluga-exp-solvable"]
    ENV = project.TetralithEnvironment(
        memory_per_cpu=f"{MEMORY_LIMIT + MEMORY_PADDING}M",
        extra_options="#SBATCH -A naiss2024-5-404",
    )
else:
    SUITE = [
        "beluga-exp-solvable:problem_0_s42_j10_r2_oc31_f4.pddl",
        "beluga-exp-solvable:problem_1_s43_j5_r2_oc51_f3.pddl",
    ]
    ENV = project.LocalEnvironment(processes=4)
    # override time limit
    TIME_LIMIT = 30
    DRIVER_OPTIONS += ["--overall-time-limit", f"{TIME_LIMIT}s"]

exp = project.Experiment(environment=ENV)

exp.add_parser(project.FastDownwardExperiment.EXITCODE_PARSER)
exp.add_parser(project.FastDownwardExperiment.TRANSLATOR_PARSER)
exp.add_parser(project.FastDownwardExperiment.SINGLE_SEARCH_PARSER)
exp.add_parser(parser.get_parser())

exp.add_resource("symk", project.SIF_SYMK, symlink=True)

# Experiments with symk
symk_configs = [
    (
        "symk-fw",
        [
            "--search",
            "sym_fw()",
        ],
    ),
    (
        "symk-bd",
        [
            "--search",
            "sym_bd()",
        ],
    ),
    (
        "astar-lmcut",
        [
            "--search",
            "astar(lmcut())",
        ],
    ),
]

symk_driver_options = DRIVER_OPTIONS

for config_name, config in symk_configs:
    for instance in suites.build_suite(BENCHMARK_DIR, SUITE):
        config_driver_options = symk_driver_options

        run = exp.add_run()
        add_resources(run, instance)
        set_properties(run, instance, config_name, config, config_driver_options)

        cmd = (
            project.get_bind_cmd()
            + ["{symk}"]
            + config_driver_options
            + ["{domain}", "{problem}"]
            + config
        )

        run.add_command(
            "planner",
            project.get_cmd_with_timeout(cmd, f"{TIME_LIMIT}s"),
            time_limit=TIME_LIMIT,
            memory_limit=MEMORY_LIMIT,
        )

exp.add_step("build", exp.build)
exp.add_step("start", exp.start_runs)
exp.add_step("parse", exp.parse)
exp.add_fetcher(name="fetch")

config_names = [x[0] for x in symk_configs]

plan_optimality_filter = OptimalityFilter()

TABLE_ATTRIBUTES = [
    "coverage",
    "run_dir",
    "time",
    "total_time",
    "plan_length",
    "cost",
    "plan",
    plan_optimality_filter.get_attribute(),
]

exp.add_report(
    AbsoluteReport(
        attributes=TABLE_ATTRIBUTES,
        filter_algorithm=config_names,
        filter=[
            plan_optimality_filter.store_attribute,
            plan_optimality_filter.check_consistency,
        ],
    )
)

exp.add_report(
    CactusPlot(
        attributes=["coverage", "total_time"],
        filter_algorithm=config_names,
    )
)

exp.run_steps()
