# Navigating the Plan Space with Facets

## Usage

Basic usage:

```
./run.py -i /path/to/instance --horizon HORIZON
```

where `HORIZON` is a positive number.

For now, we only manage to use `fasb` using commands via script, no interactive
mode. The file `script.fsb` should contain the commands you want to execute.

Other arguments:

- `--domain` specifies the domain file (automatically discovered otherwise).
- `--lp-name` specifies the name of the file used to store the logic program
  (lp) produced by `plasp`. (Default: `instance.lp`)
- `--encoding` specifies the type of sequential encoding used. Valid choices are
  `exact` and `bounded`. The first forces the solver to assign one action to
  each step of the horizon; the second allows for models where some type steps
  are not used. (We might want to frontload the actions though.)
- `--cleanup` removes the lp file specified by `--lp-name` at the end of the
  execution.
