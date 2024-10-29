# PlanPilot: Navigating the Plan Space with Facets

## Usage

Basic usage:

```
./planpilot.py -i /path/to/instance --horizon HORIZON
```

where `HORIZON` is a positive number.

Other arguments:

- `--instance` specifies the problem/instance file.
- `--domain` specifies the domain file (automatically discovered otherwise).
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

The program then executs `fasb` using its interactive mode. The original
`README.md` and `LICENSE` of `fasb` can be found in the directory
`bin/fasb-x86_64-unknown-linux-gnu`.

## `fasb` Commands

Below is a list of the "essential" commands of `fasb`. We also comment on they related to the planning context:

- `! n`: list `n` different answet sets (i.e., plans, for the encoding *with*
  time steps). If `n` is not informed, all answer sets will be listed.
- `#!`: count the number of answer sets.
- `#?`: count the number of atomic facets
- `#??`: list all facets
- `+ FACET`: activate the facet `FACET`. Use the same string for `FACET` as
  listed when using the command `#??`.
- `- FACET`: deactivate the facet `FACET`. Use the same string for `FACET` as
  listed when using the command `#??`.
- `:q`: quit `fasb`
