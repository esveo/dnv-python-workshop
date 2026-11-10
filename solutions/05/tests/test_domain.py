from grid_analysis.domain import (
    Line,
    Node,
    count_overvoltage,
    count_undervoltage,
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


# --- count_undervoltage ----------------------------------------------------


def test_nodes_below_the_band_are_counted():
    nodes = [Node("N1", 0.94), Node("N2", 1.00), Node("N3", 0.90)]

    assert count_undervoltage(nodes) == 2


def test_node_on_the_lower_limit_is_not_undervoltage():
    assert count_undervoltage([Node("N1", 0.95)]) == 0


def test_overvoltage_is_not_counted_as_undervoltage():
    assert count_undervoltage([Node("N1", 1.10)]) == 0


def test_no_nodes_gives_zero_undervoltage():
    assert count_undervoltage([]) == 0


def test_custom_lower_limit_is_used():
    assert count_undervoltage([Node("N1", 0.96)], min_pu=0.97) == 1


# --- count_overvoltage -----------------------------------------------------


def test_nodes_above_the_band_are_counted():
    nodes = [Node("N1", 1.06), Node("N2", 1.00), Node("N3", 1.10)]

    assert count_overvoltage(nodes) == 2


def test_node_on_the_upper_limit_is_not_overvoltage():
    assert count_overvoltage([Node("N1", 1.05)]) == 0


def test_undervoltage_is_not_counted_as_overvoltage():
    assert count_overvoltage([Node("N1", 0.90)]) == 0


def test_no_nodes_gives_zero_overvoltage():
    assert count_overvoltage([]) == 0


def test_custom_upper_limit_is_used():
    assert count_overvoltage([Node("N1", 1.04)], max_pu=1.03) == 1
