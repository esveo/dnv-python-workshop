"""Entry point for ``python -m grid_analysis``.

Usage::

    uv run python -m grid_analysis             # project "North Grid"
    uv run python -m grid_analysis peak-load   # project "North Grid Peak Load"
    uv run python -m grid_analysis light-load  # project "North Grid Light Load"
"""

import sys

from grid_analysis.data_source import connect, load_lines, load_nodes
from grid_analysis.report import build_report

PROJECTS = {
    "normal": "North Grid",
    "peak-load": "North Grid Peak Load",
    "light-load": "North Grid Light Load",
}


def main() -> None:
    scenario = sys.argv[1] if len(sys.argv) > 1 else "normal"
    if scenario not in PROJECTS:
        sys.exit(f"Unknown scenario '{scenario}'. Available: {', '.join(PROJECTS)}")

    project = PROJECTS[scenario]
    app = connect(project)
    print(
        build_report(load_nodes(app), load_lines(app), title=f"Grid analysis {project}")
    )


if __name__ == "__main__":
    main()
