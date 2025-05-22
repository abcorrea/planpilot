import random
from optimal_plans import OPTIMAL_PLANS

random.seed(2025)


def _select_random_action_prefixes(domain_name, problem_name, fractions):
    """
    For a given domain and problem, randomly shuffles the plan and returns
    prefixes of it based on the given list of fractions.

    Each returned prefix is a list of (time_step, action) pairs.
    """
    assert all(0 <= f <= 1 for f in fractions), "Fractions must be in [0, 1]"

    plan_key = f"{domain_name}:{problem_name}"
    full_plan = OPTIMAL_PLANS[plan_key]
    assert full_plan, f"No plan found for key: {plan_key}"

    indexed_plan = list(enumerate(full_plan))
    random.shuffle(indexed_plan)

    result_prefixes = []
    for fraction in sorted(fractions):
        cutoff = int(len(indexed_plan) * fraction)
        current_prefix = indexed_plan[:cutoff]
        result_prefixes.append(current_prefix)

        # Ensure monotonicity: each prefix must contain all actions from the previous one
        if len(result_prefixes) >= 2:
            assert set(result_prefixes[-2]).issubset(set(result_prefixes[-1]))

    return result_prefixes


def _generate_occurs_constraint(action_str, time_step):
    """
    Converts an action string like 'stack c b' and a time step into a constraint:
    ':- not occurs(action(("stack","c","b")),t).'
    """
    parts = action_str.split()
    quoted_args = ",".join(f'"{arg}"' for arg in parts)
    return f":- not occurs(action(({quoted_args})), {time_step + 1})."


def get_occurs_constraints(domain_name, problem_name, fractions):
    """
    For a given domain/problem and list of fractions, return a list of strings where each string
    contains constraints that enforce the occurrence of a subset of actions from an optimal plan.
    """
    action_prefixes = _select_random_action_prefixes(
        domain_name, problem_name, fractions
    )

    constraint_sets = []
    for action_set in action_prefixes:
        constraint_block = "\n".join(
            _generate_occurs_constraint(action_str, time_step)
            for time_step, action_str in action_set
        )
        constraint_sets.append(constraint_block)

    return constraint_sets
