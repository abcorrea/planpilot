NO_KNOWN_BOUND = float("inf")
UNSOLVABLE = -1

UPPER_BOUNDS = {
    "beluga-exp-solvable:problem_1_s43_j5_r2_oc51_f3.pddl": 30,
}


def get_upper_bound(domain, problem):
    key = f"{domain}:{problem}"
    assert key in UPPER_BOUNDS
    return UPPER_BOUNDS[key]
