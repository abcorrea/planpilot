# PlanPilot: Navigating the Plan Space with Facets

PlanPilot is a tool that allows the user to interactively navigate on the *plan
space* of a planning problem. For example, the user can interactively
(de)activate *facets* of the plans, in order to understand the plan space
better.

Right now, PlanPilot supports classical planning problems described in PDDL.

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

Below is a list of the "essential" commands of `fasb`. We also comment on they related to the planning context:

- `! n`: list `n` different answet sets (*plans*, in our context). If `n` is not informed,
  all answer sets will be listed.
- `#!`: count the number of answer sets.
- `#?`: count the number of atomic facets
- `#??`: list all facets
- `+ FACET`: activate the facet `FACET`. Use the same string for `FACET` as
  listed when using the command `#??`.
- `- FACET`: deactivate the facet `FACET`. Use the same string for `FACET` as
  listed when using the command `#??`.
- `:q`: quit `fasb`


## References

- Yannis Dimopoulos, Martin Gebser, Patrick Lühne, Javier Romero, Torsten Schaub:
plasp 3: Towards Effective ASP Planning. Theory Pract. Log. Program. 19(3): 477-504 (2019)

- Johannes Klaus Fichte, Sarah Alice Gaggl, Dominik Rusovac.
Rushing and Strolling among Answer Sets - Navigation Made Easy. AAAI 2022: 5651-5659

- Martin Gebser, Roland Kaminski, Murat Knecht, Torsten Schaub:
plasp: A Prototype for PDDL-Based Planning in ASP. LPNMR 2011: 358-363
