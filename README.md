# PlanPilot: Navigating the Plan Space with Facets

## Usage

Basic usage:

```
./planpilot.py -i /path/to/instance --horizon HORIZON
```

where `HORIZON` is a positive number.

For now, we only manage to use `fasb` using commands via script, no interactive
mode. The file `script.fsb` should contain the commands you want to execute.

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
