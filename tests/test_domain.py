from grid_analysis.domain import within_voltage_band


def test_nominal_voltage_is_within_band():
    assert within_voltage_band(1.00)
