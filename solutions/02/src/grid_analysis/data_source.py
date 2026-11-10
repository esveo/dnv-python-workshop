"""Data source: the only place with access to PowerFactory.

This module translates PowerFactory objects into the data classes ``Node``
and ``Line``. No other module knows about PowerFactory.

In real use only the import changes:

    import sys
    sys.path.append(r"C:\\Program Files\\DIgSILENT\\PowerFactory 2024\\Python\\3.12")
    import powerfactory
"""

from grid_analysis import powerfactory_fake as powerfactory
from grid_analysis.domain import Line, Node


def connect(project: str) -> powerfactory.Application:
    """Activate the project and run the load flow."""
    app = powerfactory.GetApplication()
    if app.ActivateProject(project) != 0:
        raise ValueError(f"Project '{project}' could not be activated")
    if app.GetFromStudyCase("ComLdf").Execute() != 0:
        raise RuntimeError("The load flow failed")
    return app


def load_nodes(app: powerfactory.Application) -> list[Node]:
    """Read all nodes with their voltage in p.u."""
    return [
        Node(obj.loc_name, obj.GetAttribute("m:u"))
        for obj in app.GetCalcRelevantObjects("*.ElmTerm")
    ]


def load_lines(app: powerfactory.Application) -> list[Line]:
    """Read all lines with their loading in percent."""
    return [
        Line(obj.loc_name, obj.GetAttribute("c:loading"))
        for obj in app.GetCalcRelevantObjects("*.ElmLne")
    ]
