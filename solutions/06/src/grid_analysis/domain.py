"""Domain logic: checks and calculations on load flow results."""

import math
from dataclasses import dataclass

MIN_VOLTAGE_PU = 0.95
MAX_VOLTAGE_PU = 1.05
MAX_LOADING_PERCENT = 100.0

SQRT_3 = math.sqrt(3)
WATTS_PER_KILOWATT = 1000


@dataclass(frozen=True)
class Node:
    """A grid node with its voltage in p.u."""

    name: str
    voltage_pu: float


@dataclass(frozen=True)
class Line:
    """A line with its loading in percent."""

    name: str
    loading_percent: float


def within_voltage_band(
    voltage_pu: float, min_pu: float = MIN_VOLTAGE_PU, max_pu: float = MAX_VOLTAGE_PU
) -> bool:
    """Check whether a node voltage lies within the permitted band.

    Voltages in p.u. (per unit), the limits belong to the band.
    """
    return min_pu <= voltage_pu <= max_pu


def is_overloaded(
    loading_percent: float, limit_percent: float = MAX_LOADING_PERCENT
) -> bool:
    """Check whether a loading reaches or exceeds the limit.

    Both values in percent, the limit itself counts as overloaded.
    """
    return loading_percent >= limit_percent


def overloaded_lines(lines: list[Line], limit_percent: float) -> list[Line]:
    """Return all lines whose loading reaches or exceeds the limit."""
    return [line for line in lines if line.loading_percent >= limit_percent]


def count_undervoltage(nodes: list[Node], min_pu: float = MIN_VOLTAGE_PU) -> int:
    """Count the nodes whose voltage lies below the voltage band.

    Parameters
    ----------
    nodes
        Nodes to check.
    min_pu
        Lower limit of the voltage band in p.u. The limit itself belongs to the band.

    Returns
    -------
    int
        Number of nodes with a voltage below ``min_pu``.
    """
    return sum(1 for node in nodes if node.voltage_pu < min_pu)


def count_overvoltage(nodes: list[Node], max_pu: float = MAX_VOLTAGE_PU) -> int:
    """Count the nodes whose voltage lies above the voltage band.

    Parameters
    ----------
    nodes
        Nodes to check.
    max_pu
        Upper limit of the voltage band in p.u. The limit itself belongs to the band.

    Returns
    -------
    int
        Number of nodes with a voltage above ``max_pu``.
    """
    return sum(1 for node in nodes if node.voltage_pu > max_pu)


def mean_voltage_pu(nodes: list[Node]) -> float:
    """Mean of the node voltages in p.u., 0 for an empty list."""
    if not nodes:
        return 0.0
    return math.fsum(node.voltage_pu for node in nodes) / len(nodes)


def find_node(nodes: list[Node], name: str) -> Node | None:
    """Look up a node by its name, ``None`` if there is no such node."""
    for node in nodes:
        if node.name == name:
            return node
    return None


def collect_names(lines: list[Line]) -> list[str]:
    """Return the names of the lines as a new list."""
    return [line.name for line in lines]


def three_phase_active_power_kw(
    voltage_v: float, current_a: float, power_factor: float
) -> float:
    """Active power in a three-phase system in kW: P = √3 · U · I · cos φ.

    Voltage in V (line-to-line), current in A, power factor cos φ without unit.
    """
    return SQRT_3 * voltage_v * current_a * power_factor / WATTS_PER_KILOWATT


@dataclass(frozen=True)
class CheckResult:
    """Result of a grid check: every node and line that violates a limit."""

    undervoltage: list[Node]
    overvoltage: list[Node]
    overloaded: list[Line]

    @property
    def violation_count(self) -> int:
        """Total number of violations."""
        return len(self.undervoltage) + len(self.overvoltage) + len(self.overloaded)


def check_grid(
    nodes: list[Node],
    lines: list[Line],
    min_pu: float = MIN_VOLTAGE_PU,
    max_pu: float = MAX_VOLTAGE_PU,
    limit_percent: float = MAX_LOADING_PERCENT,
) -> CheckResult:
    """Check all nodes against the voltage band and all lines against the loading limit.

    Parameters
    ----------
    nodes
        Nodes with their voltage in p.u.
    lines
        Lines with their loading in percent.
    min_pu, max_pu
        Limits of the voltage band in p.u. The limits belong to the band.
    limit_percent
        Loading limit in percent. The limit itself counts as overloaded.

    Returns
    -------
    CheckResult
        The violations, each list in the original order.
    """
    return CheckResult(
        undervoltage=[node for node in nodes if node.voltage_pu < min_pu],
        overvoltage=[node for node in nodes if node.voltage_pu > max_pu],
        overloaded=overloaded_lines(lines, limit_percent),
    )
