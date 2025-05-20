from collections import defaultdict
from lab.reports import Attribute


class RelativeFilter:
    def __init__(self, attribute):
        self.attribute = attribute
        self.cov_per_alg = defaultdict(list)

    def _get_key(self, run):
        return (run["domain"], run["problem"])

    def store_attribute(self, run):
        value = run.get(self.attribute)
        if value is not None:
            self.cov_per_alg[self._get_key(run)].append(value)
        return True

    def check_consistency(self, run):
        value = run.get(self.attribute)
        if value is not None:
            run[f"{self.attribute}_ok"] = all(
                [x == value for x in self.cov_per_alg[self._get_key(run)]]
            )
        return run

    def get_attribute(self):
        return Attribute(
            f"{self.attribute}_ok", absolute=True, min_wins=None, function=all
        )


class OptimalityFilter(RelativeFilter):
    def __init__(self):
        super().__init__("cost")


class PlanNumberFilter(RelativeFilter):
    def __init__(self):
        super().__init__("num_plans")

