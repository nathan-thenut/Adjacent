import json
import numpy as np
import matplotlib.pyplot as plt
from enum import Enum
from pathlib import Path
from datetime import datetime
from adjacent_api import *


class Result(Enum):
    ORIGINAL = 1
    L1 = 2
    L2 = 3


class PyConstraints(str, Enum):
    LENGTH = "LENGTH"
    ORTHOGONAL = "ORTHOGONAL"
    COINCIDENT = "COINCIDENT"
    POINTON = "POINTON"
    EQUAL = "EQUAL"
    ANGLE = "ANGLE"
    CENTER_TRIANGLE = "CENTER_TRIANGLE"
    MIDPOINT = "MIDPOINT"


# helper function
def point(name, xyz=(0, 0, 0)):
    """Creates a point using Adjacent's point entity."""
    if len(xyz) <= 2:
        xyz = (*xyz, 0)
    return Point(Param(f"{name}_x", xyz[0]), Param(f"{name}_y", xyz[1]),
                 Param(f"{name}_z", xyz[2]))


def circle(name, center, radius):
    """Creates a circle using Adjacent's circle entity."""
    return Circle(center, Param(f"{name}_rad", radius))


def add_lines_to_plot(figure_or_ax,
                      lines: dict[str, Line],
                      three_d: bool = False):
    """Add Lines from Adjacent to a matplotlib plot."""
    for key in lines.keys():
        source_coords = lines[key].source().eval()
        target_coords = lines[key].target().eval()
        l_x = [source_coords[0], target_coords[0]]
        l_y = [source_coords[1], target_coords[1]]
        l_z = [source_coords[2], target_coords[2]]

        if three_d:
            figure_or_ax.scatter(l_x, l_y, l_z)
            figure_or_ax.plot(l_x, l_y, l_z, label=key)
        else:
            figure_or_ax.scatter(l_x, l_y)
            figure_or_ax.plot(l_x, l_y, label=key)


def add_circles_to_plot(figure_or_ax, circles: dict[str, Circle]):
    """Add Circles from Adjacent to a matplotlib plot."""
    for key in circles.keys():
        center_coords = circles[key].center().eval()
        radius = circles[key].radius().eval()
        circle_plot = plt.Circle(center_coords,
                                 radius=radius,
                                 fill=False,
                                 in_layout=True,
                                 label=key)
        figure_or_ax.add_patch(circle_plot)
        figure_or_ax.scatter(center_coords[0], center_coords[1])
        figure_or_ax.set_aspect("equal", adjustable="datalim")
        figure_or_ax.autoscale()


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
            source_values = lines[key].source().eval()
            source["x"] = source_values[0]
            source["y"] = source_values[1]
            target = {}
            target_values = lines[key].target().eval()
            target["x"] = target_values[0]
            target["y"] = target_values[1]

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
            pnt_values = points[key].eval()
            pnt["x"] = pnt_values[0]
            pnt["y"] = pnt_values[1]

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

    if "points" in new_data.keys():
        for pnt in new_data["points"].keys():
            variables += 2
            points = new_data["points"]
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


def write_data_to_json_file(
        path: Path,
        data: dict[str, dict],
        timestamp: datetime = datetime.now(),
) -> Path:
    """Writes data to a json file."""
    filepath = path / (timestamp.strftime("%Y-%m-%dT%H%M") + ".json")
    with open(filepath, "w", encoding="utf8") as file:
        json_string = json.dumps(data, indent=2)
        file.write(json_string)

    return filepath


def read_sketch_from_json_data(
    file_path: Path
) -> tuple[dict[str, tuple[int]], dict[str, list[str]], dict[str, dict]]:
    """Reads json data into sketch data for the solver."""
    with open(file_path, "r", encoding="utf8") as file:
        json_data = json.load(file)
        points = {}
        if "points" in json_data.keys():
            points_data = json_data["points"]
            for key in points_data.keys():
                x = points_data[key][Result.ORIGINAL.name]["x"]
                y = points_data[key][Result.ORIGINAL.name]["y"]
                points[key] = (x, y)

        lines = {}
        if "lines" in json_data.keys():
            lines = json_data["lines"]
        constraint_dict = {}
        if "constraints" in json_data.keys():
            constraint_dict = json_data["constraints"]

        return (points, lines, constraint_dict)


def create_constraints(
    lines: dict[str, Line],
    points: dict[str, Point],
    constraint_dict: dict[str, dict],
) -> list[constraints.Constraint]:
    """Create constraints from the given data."""
    constraint_list = []
    for key in constraint_dict.keys():
        entities = []
        for entity in constraint_dict[key]["entities"]:
            if entity in lines.keys():
                entities.append(lines[entity])
            else:
                entities.append(points[entity])

        if constraint_dict[key]["type"] == PyConstraints.ORTHOGONAL:
            constraint_list.append(constraints.Orthogonal(*entities))
        elif constraint_dict[key]["type"] == PyConstraints.COINCIDENT:
            constraint_list.append(constraints.Coincident(*entities))
        elif constraint_dict[key]["type"] == PyConstraints.CENTER_TRIANGLE:
            constraint_list.append(constraints.CenterTriangle(*entities))
        elif constraint_dict[key]["type"] == PyConstraints.MIDPOINT:
            constraint_list.append(constraints.MidPoint(*entities))
        elif constraint_dict[key]["type"] == PyConstraints.POINTON:
            constraint_list.append(constraints.PointOn(*entities))
        elif constraint_dict[key]["type"] == PyConstraints.EQUAL:
            constraint_list.append(constraints.Equal(*entities))
        elif constraint_dict[key]["type"] == PyConstraints.LENGTH:
            value = constraint_dict[key]["value"]
            constraint_list.append(constraints.Length(*entities, value))
        elif constraint_dict[key]["type"] == PyConstraints.ANGLE:
            value = constraint_dict[key]["value"]
            constraint_list.append(constraints.Angle(*entities, value))

    return constraint_list


def create_and_solve_sketch(lines_dict: dict[str, list[str]],
                            circle_dict: dict[str, tuple[str, int]],
                            points_dict: dict[str, tuple[int]],
                            constraint_dict: dict[str, dict], json_path: Path):
    """Creates an adjacent sketch and solves it."""
    json_data = {}
    fig = plt.figure()
    subplot_int = 131

    for result in [Result.L1, Result.L2]:

        points = {}
        for key in points_dict.keys():
            points[key] = point(key, points_dict[key])

        lines = {}
        for key in lines_dict.keys():
            source = points[lines_dict[key][0]]
            target = points[lines_dict[key][1]]
            lines[key] = Line(source, target)

        circles = {}
        for key in circle_dict.keys():
            center = points[circle_dict[key][0]]
            radius = circle_dict[key][1]
            circles[key] = circle(name=key, center=center, radius=radius)

        constraint_list = create_constraints(lines, points, constraint_dict)
        if not json_data:
            json_data = export_entities_to_dict(points=points)
            json_data["lines"] = lines_dict
            json_data["circles"] = circle_dict
            json_data["constraints"] = constraint_dict
            ax = fig.add_subplot(subplot_int)
            subplot_int += 1
            ax.set_title("Original")
            add_lines_to_plot(ax, lines)
            add_circles_to_plot(ax, circles)

        s = Sketch()
        for line in lines.values():
            s.add_entity(line)

        for cc in circles.values():
            s.add_entity(cc)

        for constraint in constraint_list:
            if not isinstance(constraint, constraints.PointOn):
                s.add_constraint(constraint)

        # And solve!
        if result == Result.L1:
            s.use_linear_program(True)
        else:
            s.use_linear_program(False)
        s.update()

        for constraint in constraint_list:
            if isinstance(constraint, constraints.PointOn):
                s.add_constraint(constraint)
        s.update()

        ax2 = fig.add_subplot(subplot_int)
        subplot_int += 1
        ax2.set_title(f"{result.name}")
        add_lines_to_plot(ax2, lines)
        add_circles_to_plot(ax2, circles)

        json_data = export_entities_to_dict(points=points,
                                            data=json_data,
                                            result=result)

    json_data = add_comparison_data(json_data)
    check_angle_constraints(json_data)
    file_path = write_data_to_json_file(path=json_path, data=json_data)
    # plt.legend()
    plt.show()

    return file_path


def get_angle_between_vectors(vector1, vector2) -> float:
    """Calculate angle between two vectors."""
    v1_angle_to_x = np.rad2deg(np.arctan2(vector1[0], vector1[1]))
    v2_angle_to_x = np.rad2deg(np.arctan2(vector2[0], vector2[1]))

    return max(v1_angle_to_x, v2_angle_to_x) - min(v1_angle_to_x,
                                                   v2_angle_to_x)


def check_angle_constraints(data: dict[str, dict]):
    """Calculate the angles and check if constraints have been met."""
    for constraint in data["constraints"].keys():
        c = data["constraints"][constraint]
        if c["type"] in [PyConstraints.ANGLE, PyConstraints.ORTHOGONAL]:
            if c["type"] == PyConstraints.ANGLE:
                c["value_in_deg"] = np.rad2deg(c["value"])
            lines = {}
            for line in c["entities"]:
                line_data = data["lines"][line]
                for pnt in line_data:
                    point_data = data["points"][pnt]
                    for result in point_data.keys():
                        if result not in lines.keys():
                            lines[result] = {}
                        if line not in lines[result].keys():
                            lines[result][line] = {}
                        lines[result][line][pnt] = point_data[result]

            for result in lines.keys():
                vectors = []
                for line in lines[result].keys():
                    line_data = lines[result][line]
                    pnts = list(line_data.keys())
                    start_x = line_data[pnts[0]]["x"]
                    start_y = line_data[pnts[0]]["y"]
                    end_x = line_data[pnts[1]]["x"]
                    end_y = line_data[pnts[1]]["y"]
                    vectors.append((start_x - end_x, start_y - end_y))
                c[result] = get_angle_between_vectors(*vectors)
