"""Output: turns the results into a short text report."""

import os
from grid_analysis.domain import (
    MAX_LOADING_PERCENT,
    MAX_VOLTAGE_PU,
    MIN_VOLTAGE_PU,
    Line,
    Node,
    collect_names,
    mean_voltage_pu,
    overloaded_lines,
    within_voltage_band,
)


def share_percent(part: int, total: int) -> int:
    """Share in percent."""
    return part / total * 100


def formatLine(Name: str, value: str) -> str:
    return f"  {Name:<20}{value:>12}"


def build_report(nodes: list[Node], lines: list[Line], title: str | None = None) -> str:
    """Build the report as text with one row per finding."""
    if title is None:
        title = "Grid analysis"

    total = len(nodes) + len(lines)
    violations = [node for node in nodes if not within_voltage_band(node.voltage_pu)]
    overloaded = overloaded_lines(lines, MAX_LOADING_PERCENT)

    rows = [title, "=" * len(title), f""]
    rows.append(f"Nodes: {len(nodes)}, mean voltage: {mean_voltage_pu(nodes):.3f} p.u.")
    if nodes:
        within_band = share_percent(len(nodes) - len(violations), len(nodes))
        rows.append(f"Within voltage band: {within_band:.0f} %")
    rows.append(f"Lines: {len(lines)}")

    rows.append("")
    rows.append(f"Voltage band violations ({MIN_VOLTAGE_PU} to {MAX_VOLTAGE_PU} p.u.):")
    for node in violations:
        rows.append(formatLine(node.name, f"{node.voltage_pu:.3f} p.u."))
    if not violations:
        rows.append("  none")

    rows.append("")
    rows.append(f"Overloaded lines (from {MAX_LOADING_PERCENT:.0f} %):")
    for line in overloaded:
        rows.append(formatLine(line.name, f"{line.loading_percent:.1f} %"))
    if not overloaded:
        rows.append("  none")

    rows.append("")
    rows.append(f"Overloaded: {', '.join(collect_names(overloaded)) or 'none'}")
    return "\n".join(rows)
