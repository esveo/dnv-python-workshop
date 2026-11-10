from grid_analysis.domain import (
    Line,
    is_overloaded,
    overloaded_lines,
    within_voltage_band,
)

# --- within_voltage_band ---------------------------------------------------


def test_nominal_voltage_is_within_band():
    assert within_voltage_band(1.00)


def test_undervoltage_is_outside_band():
    assert not within_voltage_band(0.94)


def test_overvoltage_is_outside_band():
    assert not within_voltage_band(1.06)


def test_lower_limit_belongs_to_band():
    assert within_voltage_band(0.95)


def test_upper_limit_belongs_to_band():
    assert within_voltage_band(1.05)


def test_missing_measurement_is_not_within_band():
    assert not within_voltage_band(float("nan"))


def test_custom_limits_replace_the_defaults():
    assert within_voltage_band(0.92, min_pu=0.90, max_pu=1.10)


# --- is_overloaded ---------------------------------------------------------


def test_loading_below_limit_is_not_overloaded():
    assert not is_overloaded(99.9)


def test_loading_above_limit_is_overloaded():
    assert is_overloaded(100.1)


def test_loading_exactly_on_limit_is_overloaded():
    assert is_overloaded(100.0)


def test_custom_limit_is_used():
    assert is_overloaded(85.0, limit_percent=80.0)


def test_loading_below_custom_limit_is_not_overloaded():
    assert not is_overloaded(75.0, limit_percent=80.0)


# --- overloaded_lines ------------------------------------------------------


def test_only_lines_at_or_above_the_limit_are_returned():
    lines = [Line("L1", 80.0), Line("L2", 120.0), Line("L3", 99.9)]

    assert overloaded_lines(lines, limit_percent=100.0) == [Line("L2", 120.0)]


def test_line_exactly_on_the_limit_counts_as_overloaded():
    lines = [Line("L1", 100.0)]

    assert overloaded_lines(lines, limit_percent=100.0) == [Line("L1", 100.0)]


def test_empty_list_gives_empty_list():
    assert overloaded_lines([], limit_percent=100.0) == []


def test_no_line_overloaded_gives_empty_list():
    lines = [Line("L1", 10.0), Line("L2", 99.0)]

    assert overloaded_lines(lines, limit_percent=100.0) == []


def test_all_lines_overloaded_keeps_the_original_order():
    lines = [Line("L3", 130.0), Line("L1", 110.0), Line("L2", 150.0)]

    result = overloaded_lines(lines, limit_percent=100.0)

    assert [line.name for line in result] == ["L3", "L1", "L2"]


def test_limit_is_taken_from_the_parameter():
    lines = [Line("L1", 80.0), Line("L2", 60.0)]

    assert overloaded_lines(lines, limit_percent=70.0) == [Line("L1", 80.0)]


def test_input_list_is_not_modified():
    lines = [Line("L1", 80.0), Line("L2", 120.0)]

    overloaded_lines(lines, limit_percent=100.0)

    assert lines == [Line("L1", 80.0), Line("L2", 120.0)]
