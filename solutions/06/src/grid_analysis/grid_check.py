"""Check report for a grid: the imperative shell.

This module only wires things together. It fetches the data, reads the time,
calls the pure core in ``domain.py`` and writes the file.

Usage: uv run python -m grid_analysis.grid_check
"""

from datetime import datetime
from pathlib import Path

from grid_analysis.data_source import DataSource, PowerFactoryDataSource, connect
from grid_analysis.domain import CheckResult, check_grid
from grid_analysis.report import format_check_report, write_report


def check(source: DataSource) -> CheckResult:
    """Load nodes and lines from the data source and check them."""
    return check_grid(source.load_nodes(), source.load_lines())


def create_check_report(source: DataSource, now: datetime, path: Path) -> CheckResult:
    """Check the grid and write the report to ``path``."""
    result = check(source)
    write_report(format_check_report(result, now), path)
    return result


def main() -> None:
    app = connect("North Grid Peak Load")
    path = Path("check_report.txt")
    create_check_report(PowerFactoryDataSource(app), datetime.now(), path)
    app.PrintPlain(f"Report written: {path}")


if __name__ == "__main__":
    main()
