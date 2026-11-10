"""A stand-in for the most important parts of the PowerFactory Python API.

The real ``powerfactory`` module only exists with a PowerFactory licence.
This module mimics enough of it that the exercises run without a licence
while the code still looks like a real script::

    app = powerfactory.GetApplication()
    app.ActivateProject("North Grid")
    app.GetFromStudyCase("ComLdf").Execute()
    for node in app.GetCalcRelevantObjects("*.ElmTerm"):
        print(node.loc_name, node.GetAttribute("m:u"))

Mimicked are:

- ``GetApplication()``
- ``Application.ActivateProject``, ``GetFromStudyCase("ComLdf")``,
  ``GetCalcRelevantObjects("*.ElmTerm")`` / ``("*.ElmLne")``, ``PrintPlain``
- ``ComLdf.Execute``
- ``DataObject.loc_name``, ``GetClassName``, ``GetAttribute("m:u")`` (nodes)
  and ``GetAttribute("c:loading")`` (lines)

As in the real PowerFactory, results only exist after the load flow has run.

Everything starting with ``fake_`` does not exist in the real PowerFactory.
These functions provide large test data for the NumPy and scenario exercises.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

# Each project stands for one scenario of the same small grid.
_NODE_VOLTAGES_PU: dict[str, dict[str, float]] = {
    "North Grid": {
        "SUB North": 1.020,
        "BUS Harbour": 1.004,
        "BUS Market": 0.991,
        "BUS Station": 0.978,
        "BUS Plant": 0.962,
        "BUS East": 0.985,
        "BUS South": 0.943,
        "BUS West": 1.012,
    },
    "North Grid Peak Load": {
        "SUB North": 1.010,
        "BUS Harbour": 0.987,
        "BUS Market": 0.968,
        "BUS Station": 0.951,
        "BUS Plant": 0.934,
        "BUS East": 0.962,
        "BUS South": 0.917,
        "BUS West": 0.995,
    },
    "North Grid Light Load": {
        "SUB North": 1.040,
        "BUS Harbour": 1.047,
        "BUS Market": 1.038,
        "BUS Station": 1.031,
        "BUS Plant": 1.026,
        "BUS East": 1.035,
        "BUS South": 1.022,
        "BUS West": 1.058,
    },
}

_LINE_LOADINGS_PERCENT: dict[str, dict[str, float]] = {
    "North Grid": {
        "L1 North-Harbour": 72.5,
        "L2 Harbour-Market": 64.0,
        "L3 Market-Station": 88.3,
        "L4 Station-Plant": 104.2,
        "L5 Plant-South": 57.9,
        "L6 North-West": 41.6,
    },
    "North Grid Peak Load": {
        "L1 North-Harbour": 96.8,
        "L2 Harbour-Market": 87.1,
        "L3 Market-Station": 112.4,
        "L4 Station-Plant": 131.0,
        "L5 Plant-South": 79.3,
        "L6 North-West": 58.2,
    },
    "North Grid Light Load": {
        "L1 North-Harbour": 31.2,
        "L2 Harbour-Market": 27.5,
        "L3 Market-Station": 38.0,
        "L4 Station-Plant": 44.9,
        "L5 Plant-South": 24.1,
        "L6 North-West": 18.7,
    },
}

PROJECTS = tuple(_NODE_VOLTAGES_PU)


class DataObject:
    """A grid element, e.g. a node (``ElmTerm``) or a line (``ElmLne``)."""

    def __init__(
        self,
        app: Application,
        loc_name: str,
        class_name: str,
        results: dict[str, float],
    ):
        self.loc_name = loc_name
        self._app = app
        self._class_name = class_name
        self._results = results

    def GetClassName(self) -> str:
        return self._class_name

    def GetAttribute(self, name: str) -> float:
        """Return a result quantity, e.g. ``"m:u"`` or ``"c:loading"``."""
        if name not in self._results:
            raise AttributeError(
                f"{self._class_name} '{self.loc_name}' has no attribute '{name}'"
            )
        if not self._app._load_flow_done:
            raise AttributeError(
                f"'{name}' is not available yet: run the load flow first (ComLdf.Execute())"
            )
        return self._results[name]

    def __repr__(self) -> str:
        return f"<{self._class_name} {self.loc_name}>"


class ComLdf:
    """The load flow command."""

    def __init__(self, app: Application):
        self._app = app

    def Execute(self) -> int:
        """Run the load flow. Return value 0 means success."""
        if self._app._project is None:
            return 1
        self._app._load_flow_done = True
        return 0


class Application:
    """The application object returned by ``GetApplication()``."""

    def __init__(self) -> None:
        self._project: str | None = None
        self._load_flow_done = False

    def ActivateProject(self, name: str) -> int:
        """Activate a project. Return value 0 means success, 1 means not found."""
        if name not in _NODE_VOLTAGES_PU:
            return 1
        self._project = name
        self._load_flow_done = False
        return 0

    def GetFromStudyCase(self, class_name: str) -> ComLdf:
        if class_name != "ComLdf":
            raise ValueError(f"The fake module only knows 'ComLdf', not '{class_name}'")
        return ComLdf(self)

    def GetCalcRelevantObjects(
        self, name_filter: str = "*.ElmTerm"
    ) -> list[DataObject]:
        """Return all elements of a class, e.g. ``"*.ElmTerm"`` or ``"*.ElmLne"``."""
        if self._project is None:
            return []
        if name_filter == "*.ElmTerm":
            return [
                DataObject(self, name, "ElmTerm", {"m:u": voltage_pu})
                for name, voltage_pu in _NODE_VOLTAGES_PU[self._project].items()
            ]
        if name_filter == "*.ElmLne":
            return [
                DataObject(self, name, "ElmLne", {"c:loading": loading_percent})
                for name, loading_percent in _LINE_LOADINGS_PERCENT[
                    self._project
                ].items()
            ]
        raise ValueError(
            f"The fake module only knows '*.ElmTerm' and '*.ElmLne', not '{name_filter}'"
        )

    def PrintPlain(self, text: str) -> None:
        """Write a line to the PowerFactory output window."""
        print(text)


_app: Application | None = None


def GetApplication() -> Application:
    """Return the application object. As in the real PowerFactory, there is only one."""
    global _app
    if _app is None:
        _app = Application()
    return _app


# --- Large test data that does not exist like this in the real PowerFactory ---


def fake_voltages_pu(
    scenario_count: int = 1000, node_count: int = 5000, seed: int = 1
) -> NDArray[np.float64]:
    """Node voltages in p.u. for many scenarios.

    Returns an array of shape ``(scenario_count, node_count)``:
    one row per scenario, one column per node.
    """
    rng = np.random.default_rng(seed)
    return rng.normal(1.0, 0.03, size=(scenario_count, node_count))


def fake_voltage_limits_pu(
    node_count: int = 5000, seed: int = 2
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Individual voltage limits per node in p.u.

    Returns two arrays of shape ``(node_count,)``:
    first the lower limits, then the upper limits.
    """
    rng = np.random.default_rng(seed)
    lower_limits_pu = rng.choice(np.array([0.90, 0.95, 0.97]), size=node_count)
    upper_limits_pu = rng.choice(np.array([1.03, 1.05, 1.10]), size=node_count)
    return lower_limits_pu, upper_limits_pu


def fake_loadings_percent(
    scenario_count: int = 200, line_count: int = 50, seed: int = 3
) -> NDArray[np.float64]:
    """Line loadings in percent for many scenarios.

    Returns an array of shape ``(scenario_count, line_count)``:
    one row per scenario, one column per line.
    """
    rng = np.random.default_rng(seed)
    base_loading_percent = rng.uniform(30.0, 95.0, size=line_count)
    variation_percent = rng.normal(0.0, 12.0, size=(scenario_count, line_count))
    return np.clip(base_loading_percent + variation_percent, 0.0, None)


def fake_line_names(line_count: int = 50) -> list[str]:
    """Line names matching the columns of ``fake_loadings_percent``."""
    return [f"L{number:03d}" for number in range(1, line_count + 1)]


def fake_scenario_names(scenario_count: int = 200) -> list[str]:
    """Scenario names matching the rows of ``fake_loadings_percent``."""
    return [f"Scenario {number:03d}" for number in range(1, scenario_count + 1)]
