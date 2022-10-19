import json
from enum import Enum
from pathlib import Path
from datetime import datetime
from adjacent_api import *


class Result(Enum):
    ORIGINAL = 1
    L1 = 2
    L2 = 3


# helper function
def point(name, xyz=(0, 0, 0)):
    """Creates a point using Adjacent's point entity."""
    if len(xyz) <= 2:
        xyz = (*xyz, 0)
    return Point(Param(f"{name}_x", xyz[0]), Param(f"{name}_y", xyz[1]),
                 Param(f"{name}_z", xyz[2]))


def add_lines_to_plot(figure_or_ax,
                      lines: dict[str, Line],
                      three_d: bool = False):
    """Adds Lines from Adjacent to a matplotlib plot."""
    for key in lines.keys():
        l_x = [lines[key].source().x(), lines[key].target().x()]
        l_y = [lines[key].source().y(), lines[key].target().y()]
        l_z = [lines[key].source().z(), lines[key].target().z()]

        if three_d:
            figure_or_ax.scatter(l_x, l_y, l_z)
            figure_or_ax.plot(l_x, l_y, l_z, label=key)
        else:
            figure_or_ax.scatter(l_x, l_y)
            figure_or_ax.plot(l_x, l_y, label=key)


def export_entities_to_dict(
        lines: dict[str, Line],
        points: dict[str, Point],
        data: dict[str, dict] = None,
        result: Result = Result.ORIGINAL) -> dict[str, dict]:
    """Export Adjacent's Line entity to a dictionary."""
    new_data = {}
    if data:
        new_data = data
    if lines:
        if "lines" not in new_data.keys():
            new_data["lines"] = {}
        for key in lines.keys():
            source = {}
            source["x"] = lines[key].source().x()
            source["y"] = lines[key].source().y()
            target = {}
            target["x"] = lines[key].target().x()
            target["y"] = lines[key].target().y()

            if not new_data["lines"]:
                new_data["lines"][key] = {}
                new_data["lines"][key]["points"] = {}
                new_data["lines"][key]["points"]["source"] = {}
                new_data["lines"][key]["points"]["target"] = {}

            new_data["lines"][key]["points"]["source"][result.name] = source
            new_data["lines"][key]["points"]["target"][result.name] = target

    if points:
        if "points" not in new_data.keys():
            new_data["points"] = {}
        for key in points.keys():
            pnt = {}
            pnt["x"] = points[key].x()
            pnt["y"] = points[key].y()

            if not new_data["points"]:
                new_data["points"][key] = {}
                new_data["points"][key][result.name] = {}

            new_data["points"][key][result.name] = pnt

    return new_data


def write_data_to_json(path: Path,
                       data: dict[str, dict],
                       timestamp: datetime = datetime.now()):
    """Writes data to a json file."""
    filepath = path / timestamp.strftime("%Y-%m-%dT%H%M")
    with open(filepath, "w") as file:
        json.dumps(data, file)
