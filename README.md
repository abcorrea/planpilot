# PlanPilot: Navigating the Plan Space with Facets

PlanPilot is a tool that allows the user to interactively navigate on the *plan
space* of a planning problem. For example, the user can interactively
(de)activate *facets* of the plans, in order to understand the plan space
better.

Right now, PlanPilot supports classical planning problems described in PDDL.

Official Repository: https://github.com/abcorrea/planpilot

## Usage

Basic usage:

```
./planpilot.py -i /path/to/instance.pddl --horizon HORIZON
```

where `HORIZON` is a positive number.

Other arguments:

- `--instance` specifies the PDDL problem/instance file.
- `--domain` specifies the PDDL domain file (automatically discovered otherwise).
- `--cleanup` removes the lp file specified by `--lp-name` at the end of the
  execution.
- `--encoding` specifies the type of sequential encoding used. Valid choices are
  `exact` and `bounded`. The first forces the solver to assign one action to
  each step of the horizon; the second allows for models where some type steps
  are not used. (We might want to frontload the actions though.)
- `--abstract-time-steps` uses the encoding without explicitly keeping track of
  at which time step each action is used. Instead, it just keeps track whether
  an action was used at any given step of plan.
- `--lp-name` specifies the name of the file used to store the logic program
  (lp) produced by `plasp`. (Default: `instance.lp`)

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
