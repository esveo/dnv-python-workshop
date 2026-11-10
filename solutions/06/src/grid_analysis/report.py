"""Output: turns the results into a short text report."""

from datetime import datetime
from pathlib import Path

from grid_analysis.domain import (
    MAX_LOADING_PERCENT,
    MAX_VOLTAGE_PU,
    MIN_VOLTAGE_PU,
    CheckResult,
    Line,
    Node,
    collect_names,
    mean_voltage_pu,
    overloaded_lines,
    within_voltage_band,
)


def share_percent(part: int, total: int) -> float:
    """Share in percent."""
    return part / total * 100


def format_line(name: str, value: str) -> str:
    """One report row: name on the left, value right-aligned."""
    return f"  {name:<20}{value:>12}"


def build_report(nodes: list[Node], lines: list[Line], title: str | None = None) -> str:
    """Build the report as text with one row per finding."""
    if title is None:
        title = "Grid analysis"

    violations = [node for node in nodes if not within_voltage_band(node.voltage_pu)]
    overloaded = overloaded_lines(lines, MAX_LOADING_PERCENT)

    rows = [title, "=" * len(title), ""]
    rows.append(f"Nodes: {len(nodes)}, mean voltage: {mean_voltage_pu(nodes):.3f} p.u.")
    if nodes:
        within_band = share_percent(len(nodes) - len(violations), len(nodes))
        rows.append(f"Within voltage band: {within_band:.0f} %")
    rows.append(f"Lines: {len(lines)}")

    rows.append("")
    rows.append(f"Voltage band violations ({MIN_VOLTAGE_PU} to {MAX_VOLTAGE_PU} p.u.):")
    for node in violations:
        rows.append(format_line(node.name, f"{node.voltage_pu:.3f} p.u."))
    if not violations:
        rows.append("  none")

    rows.append("")
    rows.append(f"Overloaded lines (from {MAX_LOADING_PERCENT:.0f} %):")
    for line in overloaded:
        rows.append(format_line(line.name, f"{line.loading_percent:.1f} %"))
    if not overloaded:
        rows.append("  none")

    rows.append("")
    rows.append(f"Overloaded: {', '.join(collect_names(overloaded)) or 'none'}")
    return "\n".join(rows)


def format_check_report(result: CheckResult, now: datetime) -> str:
    """Build the text of the check report.

    Parameters
    ----------
    result
        The violations found by ``check_grid``.
    now
        Time of the report. Passed in so that the function stays pure.

    Returns
    -------
    str
        The report, one row per violation.
    """
    rows = ["Check report of " + now.strftime("%d.%m.%Y %H:%M"), ""]
    for node in result.undervoltage:
        rows.append(f"{node.name}: undervoltage ({node.voltage_pu:.3f} p.u.)")
    for node in result.overvoltage:
        rows.append(f"{node.name}: overvoltage ({node.voltage_pu:.3f} p.u.)")
    for line in result.overloaded:
        rows.append(f"{line.name}: overloaded ({line.loading_percent:.1f} %)")
    rows.append("")
    rows.append(f"{result.violation_count} violations")
    return "\n".join(rows)


def write_report(text: str, path: Path) -> None:
    """Write the report to a file. The only place that touches the file system."""
    path.write_text(text, encoding="utf-8")
