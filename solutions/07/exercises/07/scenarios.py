"""Voltage band violations per scenario (solution of exercise 07).

Two versions of the same count:

- ``count_violations``: the nested Python loops from the starting code
- ``count_violations_numpy``: vectorised, without Python loops

Usage: uv run python exercises/07/scenarios.py
"""

import time

import numpy as np
from numpy.typing import NDArray

from grid_analysis.powerfactory_fake import fake_voltages_pu

MIN_VOLTAGE_PU = 0.95
MAX_VOLTAGE_PU = 1.05


def count_violations(voltages_pu: NDArray[np.float64]) -> list[int]:
    """Count the nodes outside the voltage band for every scenario.

    ``voltages_pu`` has the shape (scenarios, nodes).
    """
    result = []
    for scenario in voltages_pu:
        count = 0
        for voltage_pu in scenario:
            if voltage_pu < MIN_VOLTAGE_PU or voltage_pu > MAX_VOLTAGE_PU:
                count += 1
        result.append(count)
    return result


def count_violations_numpy(voltages_pu: NDArray[np.float64]) -> NDArray[np.int_]:
    """Count the nodes outside the voltage band for every scenario, without loops.

    Parameters
    ----------
    voltages_pu
        Node voltages in p.u., shape (scenarios, nodes).

    Returns
    -------
    NDArray[np.int_]
        Number of violations per scenario, shape (scenarios,).
    """
    # Two comparisons, each gives a boolean array of shape (scenarios, nodes).
    # "|" combines them element by element: True where either one is True.
    outside_band = (voltages_pu < MIN_VOLTAGE_PU) | (voltages_pu > MAX_VOLTAGE_PU)
    # True counts as 1. axis=1 sums along the nodes: one number per scenario.
    return outside_band.sum(axis=1)


def main() -> None:
    voltages_pu = fake_voltages_pu()
    print(f"Data: {voltages_pu.shape[0]} scenarios x {voltages_pu.shape[1]} nodes")

    start = time.perf_counter()
    violations = count_violations(voltages_pu)
    loop_duration_s = time.perf_counter() - start

    start = time.perf_counter()
    violations_numpy = count_violations_numpy(voltages_pu)
    numpy_duration_s = time.perf_counter() - start

    print(f"Loop:  {loop_duration_s:.3f} s")
    print(
        f"NumPy: {numpy_duration_s:.3f} s ({loop_duration_s / numpy_duration_s:.0f} times faster)"
    )
    print(f"Same result: {np.array_equal(violations, violations_numpy)}")
    print(f"Violations in the first five scenarios: {violations[:5]}")


if __name__ == "__main__":
    main()
