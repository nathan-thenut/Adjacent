import json
import numpy as np
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
        lines: dict[str, Line] = None,
        points: dict[str, Point] = None,
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

            if key not in new_data["lines"].keys():
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

            if key not in new_data["points"].keys():
                new_data["points"][key] = {}
                new_data["points"][key][result.name] = {}

            new_data["points"][key][result.name] = pnt

    return new_data


def add_comparison_data(data: dict[str, dict]) -> dict[str, dict]:
    """Add data to compare the different solutions."""
    new_data = data
    variables = 0
    sum_of_changes = {}
    non_zero_results = {}
    for result in [Result.L1.name, Result.L2.name]:
        sum_of_changes[result] = 0
        non_zero_results[result] = 0

    if "lines" in new_data.keys():
        for line in new_data["lines"].keys():
            points = new_data["lines"][line]["points"]
            for pnt in points.keys():
                variables += 2
                add_comparison_data_to_point(points[pnt])
                for result in [Result.L1.name, Result.L2.name]:
                    if result in points[pnt].keys():
                        sum_of_changes[result] += points[pnt][result][
                            "sum_of_changes"]
                        non_zero_results[result] += points[pnt][result][
                            "non_zero_results"]

    results = {}
    results["sum_of_changes"] = sum_of_changes
    results["non_zero_results"] = non_zero_results
    results["variables"] = variables
    new_data["Results"] = results
    return new_data


def add_comparison_data_to_point(point_data: dict[str, dict]):
    """Add comparison data to a points results"""
    original_data = point_data[Result.ORIGINAL.name]
    for result in [Result.L1.name, Result.L2.name]:
        if result in point_data.keys():
            soc = calculate_sum_of_changes(original_data, point_data[result])
            point_data[result]["sum_of_changes"] = soc
            non_zero_results = count_non_zeroes_in_result(
                original_data, point_data[result])
            point_data[result]["non_zero_results"] = non_zero_results


def calculate_sum_of_changes(
    original: dict[str, float],
    new: dict[str, float],
) -> float:
    """Calculate the sum of changes between original and new point data."""
    return np.sum(
        np.abs([
            original["x"] - new["x"],
            original["y"] - new["y"],
        ]))


def count_non_zeroes_in_result(
    original: dict[str, float],
    new: dict[str, float],
) -> int:
    """Count non zero results in points for sparsity calculation."""
    non_zero_results = 0
    for var in original.keys():
        diff = original[var] - new[var]
        if diff != 0:
            non_zero_results += 1

    return non_zero_results


def write_data_to_json_file(path: Path,
                            data: dict[str, dict],
                            timestamp: datetime = datetime.now()):
    """Writes data to a json file."""
    filepath = path / (timestamp.strftime("%Y-%m-%dT%H%M") + ".json")
    with open(filepath, "w", encoding="utf8") as file:
        json_string = json.dumps(data, indent=2)
        file.write(json_string)
