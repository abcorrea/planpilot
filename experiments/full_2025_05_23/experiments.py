#! /usr/bin/env python3

import optimal_plans
import plan_constraints
import project
import parser
import re
import sys

from cactus_plot import CactusPlot
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
    run.set_property("component_options", config[:])
    run.set_property("driver_options", config_driver_options[:])
    run.set_property("id", [config_name, instance.domain, instance.problem])


QUALITY = 1
MEMORY_LIMIT = 3584  # 3.5GiB
MEMORY_PADDING = 3584 - MEMORY_LIMIT  # TetralithEnvironment has 3872 MB per cpu
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
    TIME_LIMIT = 120
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

        # Remove all outpus.sas files
        run.add_command(
            "cleanup-output",
            [
                sys.executable,
                "-c",
                "import glob, os; [os.remove(f) for f in glob.glob('output.sas')]",
            ],
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
fixed_plan_fractions = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

planpilot_tmp_configs = [
    ("planpilot-count", ["--script", "scripts/count-sols.fasb"]),
    ("planpilot-list-facets", ["--script", "scripts/list-facets.fasb"]),
    ("planpilot-reason-facets", ["--script", "scripts/facet-reason.fasb"]),
]
planpilot_config_names = set()

for instance in suites.build_suite(BENCHMARK_DIR, SUITE):
    # Get upper bound for current instance and skip if it is unsolvable or no bound is known
    bound = optimal_plans.get_optimal_plan_cost(instance.domain, instance.problem)
    if bound is None:
        continue

    bound = int(bound * QUALITY)

    constraints = plan_constraints.get_occurs_constraints(
        instance.domain, instance.problem, fixed_plan_fractions
    )
    for fraction_id, fraction in enumerate(fixed_plan_fractions):
        for config_base_name, config in planpilot_tmp_configs:
            config_name = f"{config_base_name}-{fraction}"
            planpilot_config_names.add(config_name)

            full_config = config[:]
            full_config += ["--horizon", str(bound)]

            run = exp.add_run()
            add_resources(run, instance)
            set_properties(run, instance, config_name, full_config[:], [])
            run.set_property("bound", bound)

            full_config += ["--add-constraints", constraints[fraction_id]]

            # Clean up all the escaped and problematic characters in the constraints
            # so that they can be added to the report and displayed correctly.
            cleaned_constraints = re.sub(
                r"[^. 0-9a-z]", "", constraints[fraction_id], re.IGNORECASE
            )
            cleaned_constraints = cleaned_constraints.replace(":-", "")
            cleaned_constraints = cleaned_constraints.replace('"', "")
            cleaned_constraints = cleaned_constraints.split("\n")
            run.set_property("constraints", cleaned_constraints)

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
                # memory_limit=MEMORY_LIMIT,
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

planpilot_config_names = sorted(list(planpilot_config_names))

exp.add_step("build", exp.build)
exp.add_step("start", exp.start_runs)
exp.add_step("parse", exp.parse)
exp.add_fetcher(name="fetch")

config_names = (
    [x[0] for x in kstar_configs]
    + [x[0] for x in symk_configs]
    + [x[0] for x in planalyst_configs]
    + planpilot_config_names
)

plan_number_filter = PlanNumberFilter()
facet_number_filter = FacetNumberFilter()

TABLE_ATTRIBUTES = [
    project.Attribute("bound", function=project.statistics.mean),
    "coverage",
    project.Attribute("num_plans", min_wins=False, function=project.statistics.mean),
    project.Attribute(
        "num_facets", min_wins=False, function=project.statistics.median, absolute=True
    ),
    "facet_reason",
    "facet_list",
    "run_dir",
    "time",
    "total_time",
]

exp.add_report(
    AbsoluteReport(
        attributes=TABLE_ATTRIBUTES,
        filter_algorithm=config_names,
    ),
    name="full_report",
)

exp.add_report(
    AbsoluteReport(
        attributes=TABLE_ATTRIBUTES,
        filter_algorithm=[x[0] for x in kstar_configs]
        + [x[0] for x in symk_configs]
        + [x[0] for x in planalyst_configs]
        + [x for x in planpilot_config_names if "0.0" in x],
        filter=[
            plan_number_filter.store_attribute,
            plan_number_filter.check_consistency,
            facet_number_filter.store_attribute,
            facet_number_filter.check_consistency,
        ],
    ),
    name="complete_plan_report",
)

exp.add_report(
    AbsoluteReport(
        attributes=TABLE_ATTRIBUTES,
        filter_algorithm=planpilot_config_names,
    ),
    name="planpilot_report",
)

exp.add_report(
    AbsoluteReport(
        attributes=TABLE_ATTRIBUTES,
        filter_algorithm=[x for x in config_names if "reason-facets" in x],
    ),
    name="facet_reason_report",
)

exp.add_report(
    AbsoluteReport(
        attributes=TABLE_ATTRIBUTES,
        filter_algorithm=[x for x in config_names if "list-facets" in x],
    ),
    name="facet_list_report",
)

exp.add_report(
    CactusPlot(
        attributes=["coverage", "total_time"],
        filter_algorithm=[
            "okstar-lmcut",
            "symk-bd",
            "planalyst-ddnnf",
            "planpilot-count-0.0",
            "planpilot-count-0.5",
            "planpilot-count-0.9",
            "planpilot-reason-facets-0.0",
            "planpilot-reason-facets-0.5",
            "planpilot-reason-facets-0.9",
            "planpilot-list-facets-0.0",
            "planpilot-list-facets-0.5",
            "planpilot-list-facets-0.9",
        ],
    )
)


exp.run_steps()
