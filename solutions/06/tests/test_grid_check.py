from datetime import datetime
from pathlib import Path

from grid_analysis.domain import CheckResult, Line, Node, check_grid
from grid_analysis.grid_check import check, create_check_report
from grid_analysis.report import format_check_report


class FakeDataSource:
    """A data source for tests: returns fixed data, needs no PowerFactory."""

    def __init__(self, nodes: list[Node], lines: list[Line]):
        self.nodes = nodes
        self.lines = lines

    def load_nodes(self) -> list[Node]:
        return self.nodes

    def load_lines(self) -> list[Line]:
        return self.lines


# --- core: check_grid ------------------------------------------------------


def test_check_grid_sorts_violations_by_kind():
    nodes = [Node("N1", 0.94), Node("N2", 1.00), Node("N3", 1.06)]
    lines = [Line("L1", 80.0), Line("L2", 120.0)]

    result = check_grid(nodes, lines)

    assert result.undervoltage == [Node("N1", 0.94)]
    assert result.overvoltage == [Node("N3", 1.06)]
    assert result.overloaded == [Line("L2", 120.0)]
    assert result.violation_count == 3


def test_check_grid_treats_the_band_limits_as_permitted():
    nodes = [Node("N1", 0.95), Node("N2", 1.05)]

    result = check_grid(nodes, [])

    assert result.violation_count == 0


# --- shell with a fake data source -----------------------------------------


def test_check_finds_the_one_node_with_undervoltage():
    source = FakeDataSource(
        nodes=[Node("N1", 1.00), Node("N2", 0.93), Node("N3", 1.02)],
        lines=[],
    )

    result = check(source)

    assert [node.name for node in result.undervoltage] == ["N2"]
    assert result.violation_count == 1


def test_create_check_report_writes_the_report(tmp_path: Path):
    source = FakeDataSource(nodes=[Node("N1", 0.93)], lines=[Line("L1", 120.0)])
    path = tmp_path / "report.txt"

    create_check_report(source, now=datetime(2026, 1, 15, 9, 30), path=path)

    assert path.read_text(encoding="utf-8") == (
        "Check report of 15.01.2026 09:30\n"
        "\n"
        "N1: undervoltage (0.930 p.u.)\n"
        "L1: overloaded (120.0 %)\n"
        "\n"
        "2 violations"
    )


# --- report text -----------------------------------------------------------


def test_report_without_violations_states_zero():
    result = CheckResult(undervoltage=[], overvoltage=[], overloaded=[])

    text = format_check_report(result, now=datetime(2026, 1, 15, 9, 30))

    assert text == "Check report of 15.01.2026 09:30\n\n\n0 violations"
