#! /usr/bin/env python3

import optimal_plans
import project
import parser
import sys

from check_relative import PlanNumberFilter, FacetNumberFilter
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


QUALITY = 1
MEMORY_LIMIT = 3072  # 3GiB
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
        "beluga-exp-solvable:problem_1_s43_j5_r2_oc51_f3.pddl",
        "beluga-exp-solvable:problem_32_s75_j3_r2_oc25_f3.pddl",
    ]
    ENV = project.LocalEnvironment(processes=4)
    # override time limit
    TIME_LIMIT = 60
    DRIVER_OPTIONS += ["--overall-time-limit", f"{TIME_LIMIT}s"]

exp = project.Experiment(environment=ENV)

# exp.add_parser(project.FastDownwardExperiment.EXITCODE_PARSER)
# exp.add_parser(project.FastDownwardExperiment.TRANSLATOR_PARSER)
# exp.add_parser(project.FastDownwardExperiment.SINGLE_SEARCH_PARSER)
exp.add_parser(parser.get_parser())

exp.add_resource("planpilot", project.SIF_PLANPILOT, symlink=True)
exp.add_resource("planalyst", project.SIF_PLANALYST, symlink=True)
exp.add_resource("symk", project.SIF_SYMK, symlink=True)
exp.add_resource("kstar", project.SIF_KSTAR, symlink=True)

# Experiments with symk
symk_configs = [
    (
        "symk-bd",
        [
            "--translate-options",
            "--keep-unimportant-variables",
            "--preprocess-options",
            "--keep-unimportant-variables",
            "--search-options",
            "--search",
            "symk_bd(plan_selection=top_k(num_plans=infinity, write_plans=false), bound=XXXXX)",
        ],
    ),
]

symk_driver_options = DRIVER_OPTIONS

for config_name, config in symk_configs:
    for instance in suites.build_suite(BENCHMARK_DIR, SUITE):
        # Get upper bound for current instance and skip if it is unsolvable or no bound is known
        bound = optimal_plans.get_optimal_plan_cost(instance.domain, instance.problem)
        if bound is None:
            continue

        bound = int(bound * QUALITY)

        config_with_bound = []
        for c in config:
            config_with_bound.append(c.replace("bound=XXXXX", f"bound={bound+1}"))

        config_driver_options = symk_driver_options

        run = exp.add_run()
        add_resources(run, instance)
        set_properties(
            run, instance, config_name, config_with_bound, config_driver_options
        )
        run.set_property("bound", bound)

        cmd = (
            project.get_bind_cmd()
            + ["{symk}"]
            + config_driver_options
            + ["{domain}", "{problem}"]
            + config_with_bound
        )

        run.add_command(
            "planner",
            project.get_cmd_with_timeout(cmd, f"{TIME_LIMIT}s"),
            time_limit=TIME_LIMIT,
            memory_limit=MEMORY_LIMIT,
        )

kstar_configs = [
    (
        "okstar-lmcut",
        [
            "--translate-options",
            "--keep-unimportant-variables",
            "--search-options",
            "--symmetries",
            "sym=structural_symmetries(time_bound=0,search_symmetries=oss,stabilize_initial_state=false,keep_operator_symmetries=true)",
            "--search",
            f"kstar(lmcut(), symmetries=sym, q={QUALITY}, dump_plans=false)",
        ],
    ),
]

kstar_driver_options = DRIVER_OPTIONS

for config_name, config in kstar_configs:
    for instance in suites.build_suite(BENCHMARK_DIR, SUITE):
        # Get upper bound for current instance and skip if it is unsolvable or no bound is known
        bound = optimal_plans.get_optimal_plan_cost(instance.domain, instance.problem)
        if bound is None:
            continue

        bound = int(bound * QUALITY)

        config_driver_options = kstar_driver_options

        run = exp.add_run()
        add_resources(run, instance)
        set_properties(run, instance, config_name, config, config_driver_options)
        run.set_property("bound", bound)

        cmd = (
            project.get_bind_cmd()
            + ["{kstar}"]
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


# Experiments with Planalyst
planalyst_configs = [
    ("planalyst-ddnnf", ["--method", "ddnnf-compiler"]),
]

for config_name, config in planalyst_configs:
    for instance in suites.build_suite(BENCHMARK_DIR, SUITE):
        # Get upper bound for current instance and skip if it is unsolvable or no bound is known
        bound = optimal_plans.get_optimal_plan_cost(instance.domain, instance.problem)
        if bound is None:
            continue

        bound = int(bound * QUALITY)

        full_config = config[:]
        full_config += ["--horizon", str(bound)]

        run = exp.add_run()
        add_resources(run, instance)
        set_properties(run, instance, config_name, full_config, [])
        run.set_property("bound", bound)

        cmd = (
            project.get_bind_cmd()
            + ["{planalyst}"]
            + ["--domain", "{domain}"]
            + ["--instance", "{problem}"]
            + full_config
        )

        run.add_command(
            "planner",
            project.get_cmd_with_timeout(cmd, f"{TIME_LIMIT}s"),
            time_limit=TIME_LIMIT,
            memory_limit=MEMORY_LIMIT,
        )

        # Remove all *.cnf files
        run.add_command(
            "cleanup-cnf",
            [
                sys.executable,
                "-c",
                "import glob, os; [os.remove(f) for f in glob.glob('*.cnf')]",
            ],
        )
        # Remove gmon.out file
        run.add_command(
            "cleanup-gmon",
            [
                sys.executable,
                "-c",
                "import glob, os; [os.remove(f) for f in glob.glob('gmon.out')]",
            ],
        )

# Experiments with Planpilot
planpilot_configs = [
    ("planpilot-count", ["--script", "scripts/count-sols.fasb"]),
    ("planpilot-list-facets", ["--script", "scripts/list-facets.fasb"]),
    ("planpilot-reason-facets", ["--script", "scripts/facet-reason.fasb"]),
]

for config_name, config in planpilot_configs:
    for instance in suites.build_suite(BENCHMARK_DIR, SUITE):
        # Get upper bound for current instance and skip if it is unsolvable or no bound is known
        bound = optimal_plans.get_optimal_plan_cost(instance.domain, instance.problem)
        if bound is None:
            continue

        bound = int(bound * QUALITY)

        full_config = config[:]
        full_config += ["--horizon", str(bound)]

        run = exp.add_run()
        add_resources(run, instance)
        set_properties(run, instance, config_name, full_config, [])
        run.set_property("bound", bound)

        cmd = (
            project.get_bind_cmd()
            + ["{planpilot}"]
            + ["--domain", "{domain}"]
            + ["--instance", "{problem}"]
            + full_config
        )

        run.add_command(
            "planner",
            project.get_cmd_with_timeout(cmd, f"{TIME_LIMIT}s"),
            time_limit=TIME_LIMIT,
            memory_limit=MEMORY_LIMIT,
        )

        # Remove all outpus.sas files
        run.add_command(
            "cleanup-output",
            [
                sys.executable,
                "-c",
                "import glob, os; [os.remove(f) for f in glob.glob('output.sas')]",
            ],
        )

        # Remove instance.lp file
        run.add_command(
            "cleanup-gmon",
            [
                sys.executable,
                "-c",
                "import glob, os; [os.remove(f) for f in glob.glob('instance.lp')]",
            ],
        )

exp.add_step("build", exp.build)
exp.add_step("start", exp.start_runs)
exp.add_step("parse", exp.parse)
exp.add_fetcher(name="fetch")

config_names = (
    [x[0] for x in kstar_configs]
    + [x[0] for x in symk_configs]
    + [x[0] for x in planalyst_configs]
    + [x[0] for x in planpilot_configs]
)

plan_number_filter = PlanNumberFilter()
facet_number_filter = FacetNumberFilter()

TABLE_ATTRIBUTES = [
    project.Attribute("bound", function=project.statistics.mean),
    "coverage",
    project.Attribute("num_plans", min_wins=False, function=project.statistics.mean),
    project.Attribute("num_facets", min_wins=False, function=project.statistics.mean),
    "facet_reason",
    "facet_list",
    "run_dir",
    "time",
    "total_time",
    plan_number_filter.get_attribute(),
    facet_number_filter.get_attribute(),
]

exp.add_report(
    AbsoluteReport(
        attributes=TABLE_ATTRIBUTES,
        filter_algorithm=config_names,
        filter=[
            plan_number_filter.store_attribute,
            plan_number_filter.check_consistency,
            facet_number_filter.store_attribute,
            facet_number_filter.check_consistency,
        ],
    )
)

exp.run_steps()
