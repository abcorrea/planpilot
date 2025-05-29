# PlanPilot: Navigating the Plan Space with Facets

PlanPilot is a tool that allows the user to interactively navigate on the *plan
space* of a planning problem. For example, the user can interactively
(de)activate *facets* of the plans, in order to understand the plan space
better.

Right now, PlanPilot supports classical planning problems described in PDDL or SAS+.

## Build

The easiest way is to build an Apptainer container as follows:

```bash
apptainer build planpilot.sif Apptainer.planpilot
```

## Usage

Basic usage:

```bash
./planpilot.sif -i /path/to/instance.pddl --horizon HORIZON

```

where `HORIZON` is a positive number.

### Beluga Usage

For example, consider the Beluga Challenge with a horizon of 17 and a single fixed action at time step 12. One can enumerate or reason about the importance of the PlanPilot as follows:

```bash
./planpilot.sif -i benchmarks/beluga-exp-solvable/problem_3_s45_j3_r2_oc44_f3.pddl --horizon 17 --script scripts/list-facets.fasb --add-constraints ":- not occurs(action(("pick-up-rack","jig0002","factory_trailer_1","rack00","fside","bside","n25","n05","n30")), 12)."

./planpilot.sif -i benchmarks/beluga-exp-solvable/problem_3_s45_j3_r2_oc44_f3.pddl --horizon 17 --script scripts/facet-reason.fasb --add-constraints ":- not occurs(action(("pick-up-rack","jig0002","factory_trailer_1","rack00","fside","bside","n25","n05","n30")), 12)."
```

To start interactive mode, use the following command: Then, navigation in the plans space is possible with the `fasb` commands listed below.
```bash
./planpilot.sif -i benchmarks/beluga-exp-solvable/problem_46_s89_j3_r2_oc32_f3.pddl --horizon 17
```

### Other arguments:

- -h, --help            show this help message and exit
- -i INSTANCE, --instance INSTANCE
                        The path to the PDDL/SAS instance file.
-  -d DOMAIN, --domain DOMAIN
                        (Optional) The path to the PDDL domain file. If none is provided, the system will try to automatically deduce it from the instance filename.
-  --partial-plan PARTIAL_PLAN
                        The path to the file containing partial plan.
-  --add-constraints ADD_CONSTRAINTS
                        String containing additional constraints.
-  --add-constraints-file ADD_CONSTRAINTS_FILE
                        The path to the file containing additional constraints.
-  --dry                 If true, facets will not be computed at startup.
-  --horizon HORIZON     Horizon used by clingo.
-  --lp-name LP_NAME     Name of intermediate logic program (lp) file.
-  --encoding {exact,bounded}
                        Type of ASP encoding.
-  --abstract-time-steps
                        If true, it only reports that actions occur some time during the plans, but without specifying when.
-  --script SCRIPT       The path to the fasb script; for non-interactive mode - requires fasb built in interpreter configuration.
-  --dump-output         dump the output of tools.
-  --cleanup             Clean all LP files in the folder after execution.


The program first encodes the planning problem as an answer set program using
`plasp` (Gebser et al. 2011; Dimopoulos et al. 2019; [link to
repo](https://github.com/potassco/plasp). It then executes `fasb` (Fichte et
al. AAAI 2022; [link to repo](https://github.com/drwadu/fasb)) using its
interactive mode. The original `README.md` and `LICENSE` of `fasb` can be found
in the directory `bin/fasb-x86_64-unknown-linux-gnu`.

## `fasb` Commands

Below is a list of the "essential" commands of `fasb`. We also comment on how they relate to the planning context:

- `! n`: list `n` different answer sets (*plans*, in our context). If `n` is not given,
  all answer sets will be listed
- `?`: display all facets
- `#!`: count the number of answer sets (plans)
- `#?`: count the number of atomic facets (meaningful operators)
- `#!!`: query for each facet how much its activation decreases the number of answer sets, and the remaining number of answer sets
- `#??`: query for each facet how much its activation decreases the number of facets, and the remaining number of facets
- `+ FACET`: activate the facet `FACET`. Use the same string for `FACET` as
  listed when using the command `#??`.
- `- FACET`: deactivate the facet `FACET`. Use the same string for `FACET` as
  listed when using the command `#??`
- `:q`: quit `fasb`

## Fast Downward Translator
We utilize for grounding the [Fast Downward](https://www.fast-downward.org/latest/) translator ([files](translate)).
