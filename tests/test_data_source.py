import pytest

from grid_analysis import powerfactory_fake
from grid_analysis.data_source import connect, load_lines, load_nodes
from grid_analysis.domain import Line, Node


def test_load_nodes_translates_into_data_classes():
    app = connect("North Grid")

    nodes = load_nodes(app)

    assert len(nodes) == 8
    assert nodes[0] == Node("SUB North", 1.020)


def test_load_lines_translates_into_data_classes():
    app = connect("North Grid")

    lines = load_lines(app)

    assert len(lines) == 6
    assert lines[3] == Line("L4 Station-Plant", 104.2)


def test_unknown_project_is_rejected():
    with pytest.raises(ValueError):
        connect("Does not exist")


def test_results_only_exist_after_the_load_flow():
    app = powerfactory_fake.GetApplication()
    app.ActivateProject("North Grid")
    node = app.GetCalcRelevantObjects("*.ElmTerm")[0]

    with pytest.raises(AttributeError):
        node.GetAttribute("m:u")
