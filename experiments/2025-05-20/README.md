# Experiments

Each subfolder contains experiment scripts, gathered data, and reports for experiments on counting plans for planning tasks with unit operator costs and a dedicated plan length bound.

All experiments are run with [Lab](https://lab.readthedocs.io/en/stable/downward.tutorial.html), which can be installed using pip:

```bash
pip install lab
```

To run the experiment scripts, you need to set the following environment variables:

1. **PLANNER_IMAGES**: Points to the directory containing the three planner images (`planpilot.sif`, `planalyst.sif`, `kstar.sif`, and `symk.sif`) in the form of Apptainer/Singularity images. (See the dedicated folders for more information.)
2. **DOWNWARD_BENCHMARKS**: Points to the directory containing the [Downward benchmark set](https://github.com/aibasel/downward-benchmarks).

You can set these environment variables using the following commands:

```bash
export PLANNER_IMAGES="/path/to/images/"
export DOWNWARD_BENCHMARKS="/path/to/downward/benchmarks"
```
