from grid_analysis.domain import is_overloaded, within_voltage_band

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
