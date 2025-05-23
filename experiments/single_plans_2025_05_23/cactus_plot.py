from downward.reports import PlanningReport


TEX_HEADER = r"""
\documentclass{standalone}
\usepackage{pgfplots}

\begin{document}

\begin{tikzpicture}
\begin{axis}[
    xlabel={Time},
    ylabel={\#Solved Task},
    xmode=log,
    xmin=0,
    legend style={at={(2.0,0.5)}, anchor=east},
    grid=both,
]
"""

TEX_FOOTER = r"""
\end{axis}
\end{tikzpicture}

\end{document}
"""


class CactusPlot(PlanningReport):
    """Example plotting coverage over time:

    CactusPlot(attributes=["coverage", "planner_time"])

    """

    def __init__(self, attributes=None, max_time=1800, **kwargs):
        try:
            self.cumulative_attribute, self.time_attribute = attributes
        except ValueError:
            raise ValueError("CactusPlot needs exactly two attributes.") from None
        super().__init__(attributes=attributes, **kwargs)
        self.max_time = max_time

    def write(self):
        print(TEX_HEADER)
        print()
        for algo in self.algorithms:
            runtimes = []
            for run in self.runs.values():
                if run["algorithm"] != algo:
                    continue
                if run.get(self.cumulative_attribute):
                    runtimes.append(int(run[self.time_attribute]))
            runtimes.sort()
            cumulative_value = len(runtimes)
            coords = []
            last_runtime = None
            for runtime in reversed(runtimes):
                if last_runtime is None or runtime < last_runtime:
                    x = runtime
                    y = cumulative_value
                    coords.append((x, y))
                cumulative_value -= 1
                last_runtime = runtime
            coords = list(reversed(coords))

            # Prepend cumulative value of 0 at the first coordinate value.
            first_coord = coords[0]
            x, y = first_coord
            if x != 0:
                coords.insert(0, (x, 0))

            cumulative_value = len(runtimes)
            coord = (self.max_time, cumulative_value)
            if coords[-1] != coord:
                coords.append(coord)

            print("\\addplot coordinates {")
            for x, y in coords:
                print(f"({x}, {y})", end=" ")
            print("};")
            print(f"\\addlegendentry{{{algo}}}")
            print()
        print(TEX_FOOTER)
