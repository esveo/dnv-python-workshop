"""Output: turns the results into a short text report."""

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
