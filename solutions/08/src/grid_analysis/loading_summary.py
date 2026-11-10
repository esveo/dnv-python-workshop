"""Summary of the line loadings across all scenarios.

Pure: receives data as parameters and returns values.
Specification: docs/specs/loading.md
"""

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from grid_analysis.domain import MAX_LOADING_PERCENT


@dataclass(frozen=True)
class LineSummary:
    """Loading of one line, condensed over all scenarios."""

    name: str
    max_loading_percent: float
    overload_count: int
    most_critical_scenario: str


def summarise_loadings(
    loadings_percent: NDArray[np.float64],
    line_names: list[str],
    scenario_names: list[str],
    limit_percent: float = MAX_LOADING_PERCENT,
) -> list[LineSummary]:
    """Summarise the loading of every line across all scenarios.

    Parameters
    ----------
    loadings_percent
        Loadings in percent, shape (scenarios, lines).
    line_names
        Names of the lines, one per column.
    scenario_names
        Names of the scenarios, one per row.
    limit_percent
        Loading limit in percent. The limit itself counts as overloaded.

    Returns
    -------
    list[LineSummary]
        One entry per line, in the order of ``line_names``. With several
        scenarios of the same maximum loading, the first one is named.

    Raises
    ------
    ValueError
        If the data is not two-dimensional, the names do not match its shape,
        there are no scenarios or a value is missing (``NaN``).
    """
    if loadings_percent.ndim != 2:
        raise ValueError(
            f"loadings_percent must have two dimensions, got {loadings_percent.ndim}"
        )
    scenario_count, line_count = loadings_percent.shape
    if len(scenario_names) != scenario_count:
        raise ValueError(
            f"{len(scenario_names)} scenario names for {scenario_count} rows of data"
        )
    if len(line_names) != line_count:
        raise ValueError(
            f"{len(line_names)} line names for {line_count} columns of data"
        )
    if scenario_count == 0:
        raise ValueError("at least one scenario is needed")
    if np.isnan(loadings_percent).any():
        raise ValueError("loadings_percent contains missing values (NaN)")

    # axis=0 aggregates along the scenarios: one value per line.
    max_loadings_percent = loadings_percent.max(axis=0)
    # argmax returns the first index of the maximum, which settles ties.
    critical_indices = loadings_percent.argmax(axis=0)
    overload_counts = (loadings_percent >= limit_percent).sum(axis=0)

    return [
        LineSummary(
            name=name,
            max_loading_percent=float(max_loadings_percent[column]),
            overload_count=int(overload_counts[column]),
            most_critical_scenario=scenario_names[int(critical_indices[column])],
        )
        for column, name in enumerate(line_names)
    ]
