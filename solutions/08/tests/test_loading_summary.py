import numpy as np
import pytest

from grid_analysis.loading_summary import LineSummary, summarise_loadings
from grid_analysis.powerfactory_fake import (
    fake_line_names,
    fake_loadings_percent,
    fake_scenario_names,
)

# The example from docs/specs/loading.md: 3 scenarios x 3 lines.
LOADINGS_PERCENT = np.array(
    [
        [80.0, 100.0, 50.0],
        [120.0, 90.0, 50.0],
        [120.0, 110.0, 40.0],
    ]
)
LINE_NAMES = ["L1", "L2", "L3"]
SCENARIO_NAMES = ["Base", "Peak", "Outage"]


def test_example_from_the_specification():
    result = summarise_loadings(LOADINGS_PERCENT, LINE_NAMES, SCENARIO_NAMES)

    assert result == [
        LineSummary("L1", 120.0, 2, "Peak"),
        LineSummary("L2", 110.0, 2, "Outage"),
        LineSummary("L3", 50.0, 0, "Base"),
    ]


def test_loading_exactly_on_the_limit_counts_as_overloaded():
    result = summarise_loadings(np.array([[100.0], [99.9]]), ["L1"], ["A", "B"])

    assert result[0].overload_count == 1


def test_equal_maxima_name_the_first_scenario():
    result = summarise_loadings(
        np.array([[70.0], [90.0], [90.0]]), ["L1"], ["A", "B", "C"]
    )

    assert result[0].most_critical_scenario == "B"


def test_own_limit_is_used():
    result = summarise_loadings(
        LOADINGS_PERCENT, LINE_NAMES, SCENARIO_NAMES, limit_percent=80.0
    )

    assert [line.overload_count for line in result] == [3, 3, 0]


def test_no_lines_gives_an_empty_list():
    result = summarise_loadings(np.empty((2, 0)), [], ["A", "B"])

    assert result == []


def test_missing_value_is_rejected():
    loadings_percent = np.array([[80.0, np.nan]])

    with pytest.raises(ValueError, match="NaN"):
        summarise_loadings(loadings_percent, ["L1", "L2"], ["A"])


def test_wrong_number_of_line_names_is_rejected():
    with pytest.raises(ValueError, match="2 line names for 3 columns"):
        summarise_loadings(LOADINGS_PERCENT, ["L1", "L2"], SCENARIO_NAMES)


def test_wrong_number_of_scenario_names_is_rejected():
    with pytest.raises(ValueError, match="2 scenario names for 3 rows"):
        summarise_loadings(LOADINGS_PERCENT, LINE_NAMES, ["Base", "Peak"])


def test_no_scenarios_are_rejected():
    with pytest.raises(ValueError, match="at least one scenario"):
        summarise_loadings(np.empty((0, 2)), ["L1", "L2"], [])


def test_one_dimensional_data_is_rejected():
    with pytest.raises(ValueError, match="two dimensions"):
        summarise_loadings(np.array([80.0, 90.0]), ["L1", "L2"], ["A"])


def test_input_is_not_modified():
    loadings_percent = LOADINGS_PERCENT.copy()

    summarise_loadings(loadings_percent, LINE_NAMES, SCENARIO_NAMES)

    np.testing.assert_array_equal(loadings_percent, LOADINGS_PERCENT)


def test_fake_data_gives_one_entry_per_line():
    result = summarise_loadings(
        fake_loadings_percent(), fake_line_names(), fake_scenario_names()
    )

    assert [line.name for line in result] == fake_line_names()
    assert all(0 <= line.overload_count <= 200 for line in result)
