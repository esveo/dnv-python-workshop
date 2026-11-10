"""Domain logic: checks and calculations on load flow results."""

from dataclasses import dataclass
import math

MIN_VOLTAGE_PU = 0.95
MAX_VOLTAGE_PU = 1.05
MAX_LOADING_PERCENT = 100.0


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
    return min_pu < voltage_pu <= max_pu


def overloaded_lines(lines: list[Line], limit_percent: float) -> list[Line]:
    """Return all lines whose loading reaches or exceeds the limit."""
    return [line for line in lines if line.loading_percent >= limit_percent]


def mean_voltage_pu(nodes: list[Node]) -> float:
    """Mean of the node voltages in p.u., 0 for an empty list."""
    try:
        return math.fsum(node.voltage_pu for node in nodes) / len(nodes)
    except:
        return 0


def find_node(nodes: list[Node], name: str) -> Node:
    """Look up a node by its name."""
    for node in nodes:
        if node.name == name:
            return node


def collect_names(lines: list[Line], names: list[str] = []) -> list[str]:
    """Return the names of the lines as a list."""
    for line in lines:
        names.append(line.name)
    return names


def p(u, i, x):
    return 1.732 * u * i * x / 1000
