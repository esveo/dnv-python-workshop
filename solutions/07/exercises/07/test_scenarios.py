import numpy as np
import pytest
from numpy.testing import assert_allclose
from scenarios import (
    count_violations,
    count_violations_numpy,
    count_violations_per_node,
)

from grid_analysis.powerfactory_fake import fake_voltages_pu

# Worked out by hand: 3 scenarios x 4 nodes, band 0.95 to 1.05.
VOLTAGES_PU = np.array(
    [
        [1.00, 1.00, 1.00, 1.00],  # no violation
        [0.94, 1.00, 1.06, 1.00],  # one below, one above
        [0.95, 1.05, 0.90, 1.10],  # the limits are permitted, two violations
    ]
)
EXPECTED = [0, 2, 2]

# Read off once from the loop version for 20 scenarios x 100 nodes.
PINNED_FIRST_FIVE = [5, 8, 10, 6, 8]
PINNED_TOTAL = 197


@pytest.mark.parametrize("function", [count_violations, count_violations_numpy])
def test_example_worked_out_by_hand(function):
    assert_allclose(function(VOLTAGES_PU), EXPECTED)


def test_loop_version_keeps_its_result_for_fake_data():
    voltages_pu = fake_voltages_pu(scenario_count=20, node_count=100)

    result = count_violations(voltages_pu)

    assert_allclose(result[:5], PINNED_FIRST_FIVE)
    assert sum(result) == PINNED_TOTAL


def test_numpy_version_matches_the_loop_version():
    voltages_pu = fake_voltages_pu(scenario_count=20, node_count=100)

    assert_allclose(count_violations_numpy(voltages_pu), count_violations(voltages_pu))


def test_numpy_version_returns_one_value_per_scenario():
    voltages_pu = fake_voltages_pu(scenario_count=20, node_count=100)

    assert count_violations_numpy(voltages_pu).shape == (20,)


def test_limits_per_node_use_the_limit_of_each_column():
    voltages_pu = np.array(
        [
            [0.96, 0.96, 1.04],
            [0.93, 0.93, 1.08],
        ]
    )
    lower_limits_pu = np.array([0.95, 0.97, 0.90])
    upper_limits_pu = np.array([1.05, 1.05, 1.03])

    result = count_violations_per_node(voltages_pu, lower_limits_pu, upper_limits_pu)

    # Row 1: node 2 below 0.97, node 3 above 1.03. Row 2: all three outside.
    assert_allclose(result, [2, 3])


def test_limits_per_node_with_equal_limits_match_the_fixed_band():
    voltages_pu = fake_voltages_pu(scenario_count=20, node_count=100)
    lower_limits_pu = np.full(100, 0.95)
    upper_limits_pu = np.full(100, 1.05)

    result = count_violations_per_node(voltages_pu, lower_limits_pu, upper_limits_pu)

    assert_allclose(result, count_violations_numpy(voltages_pu))
