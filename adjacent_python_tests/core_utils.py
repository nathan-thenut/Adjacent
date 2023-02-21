from enum import Enum
from pathlib import Path
from datetime import datetime
from time import time
import json
import numpy as np
import matplotlib.pyplot as plt
from angle_annotation import AngleAnnotation
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


def get_intersection(a1, a2, b1, b2):
    """
    Returns the point of intersection of the lines passing through a2,a1 and b2,b1.
    a1: [x, y] a point on the first line
    a2: [x, y] another point on the first line
    b1: [x, y] a point on the second line
    b2: [x, y] another point on the second line
    Source: https://stackoverflow.com/questions/3252194/
            numpy-and-line-intersections/42727584#42727584
    """
    s = np.vstack([a1, a2, b1, b2])  # s for stacked
    h = np.hstack((s, np.ones((4, 1))))  # h for homogeneous
    l1 = np.cross(h[0], h[1])  # get first line
    l2 = np.cross(h[2], h[3])  # get second line
    x, y, z = np.cross(l1, l2)  # point of intersection
    if z == 0:  # lines are parallel
        return (float('inf'), float('inf'))
    return (x / z, y / z)


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
                      constraint_dict: dict[str, dict],
                      three_d: bool = False):
    """Add Lines from Adjacent to a matplotlib plot."""

    blue = '#1f77b4'
    red = 'red'
    constrained_lines = []
    for key in constraint_dict.keys():
        constraint = constraint_dict[key]
        if constraint["type"] == PyConstraints.LENGTH.name:
            constrained_lines.extend(constraint["entities"])

    for key in lines.keys():
        col = blue
        if key in constrained_lines:
            col = red

        source_coords = lines[key].source().eval()
        target_coords = lines[key].target().eval()
        l_x = [source_coords[0], target_coords[0]]
        l_y = [source_coords[1], target_coords[1]]
        l_z = [source_coords[2], target_coords[2]]

        if three_d:
            # figure_or_ax.scatter(l_x, l_y, l_z)
            figure_or_ax.plot(l_x, l_y, l_z, label=key)
        else:
            # figure_or_ax.scatter(l_x, l_y)
            figure_or_ax.plot(l_x, l_y, label=key, color=col)


def add_points_to_plot(figure_or_ax,
                       points: dict[str, Point],
                       three_d: bool = False):
    """Add Points from Adjacent to a matplotlib plot."""
    for key in points.keys():
        coords = points[key].eval()
        p_x = coords[0]
        p_y = coords[1]
        p_z = coords[2]

        if three_d:
            figure_or_ax.plot(p_x, p_y, p_z, 'ko')
            # figure_or_ax.annotate(key, (p_x, p_y, p_z), fontsize=12)
        else:
            figure_or_ax.plot(p_x, p_y, 'ko')
            # figure_or_ax.annotate(key, (p_x, p_y),
            #                       xytext=(p_x + 0.1, p_y + 0.1),
            #                       textcoords='offset points',
            #                       fontsize=12)


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


def add_annotations_for_angle_constraints(figure_or_ax, lines: dict[str, Line],
                                          constraints: dict[str, dict]):
    """Adds annotations for angle constraints to a matplotlib plot."""
    angle_constraints = [PyConstraints.ANGLE, PyConstraints.ORTHOGONAL]

    for key in constraints.keys():
        constraint = constraints[key]
        if constraint["type"] in angle_constraints:
            line1 = lines[constraint["entities"][0]]
            line2 = lines[constraint["entities"][1]]
            line1_coords = [line1.source().eval(), line1.target().eval()]
            line2_coords = [line2.source().eval(), line2.target().eval()]
            center_coords = []
            if line1_coords[0] in line2_coords:
                center_coords = line1_coords[0]
            if line1_coords[1] in line2_coords:
                center_coords = line1_coords[1]

            if not center_coords:
                center_coords = get_intersection(
                    line1_coords[0][:2],
                    line1_coords[1][:2],
                    line2_coords[0][:2],
                    line2_coords[1][:2],
                )
                print(center_coords)
                if center_coords in line1_coords:
                    line1_coords.remove(center_coords)
                    del line2_coords[0]
                elif center_coords in line2_coords:
                    line2_coords.remove(center_coords)
                    del line1_coords[0]
            else:
                line1_coords.remove(center_coords)
                line2_coords.remove(center_coords)
            if constraint["type"] == PyConstraints.ORTHOGONAL:
                value = 90
            else:
                value = int(abs(np.rad2deg(constraint["value"])))
            AngleAnnotation(center_coords[:2],
                            line2_coords[0][:2],
                            line1_coords[0][:2],
                            ax=figure_or_ax,
                            size=40,
                            color="red",
                            text=f"{value}°",
                            textposition="edge",
                            text_kw=dict(bbox=dict(boxstyle="round", fc="w")))


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
    l1_norm = {}
    l2_norm = {}
    non_zero_results = {}
    moved_points = []
    for result in [Result.L1.name, Result.L2.name]:
        l1_norm[result] = 0
        l2_norm[result] = 0
        non_zero_results[result] = 0

    if "moves" in new_data.keys():
        for move in new_data["moves"].keys():
            moved_points.append(new_data["moves"][move]["point"])

    if "points" in new_data.keys():
        for pnt in new_data["points"].keys():
            variables += 2
            points = new_data["points"]
            if pnt not in moved_points:
                add_comparison_data_to_point(points[pnt])
                for result in [Result.L1.name, Result.L2.name]:
                    if result in points[pnt].keys():
                        l1_norm[result] += points[pnt][result]["l1_norm"]
                        l2_norm[result] += points[pnt][result]["l2_norm"]
                        non_zero_results[result] += points[pnt][result][
                            "non_zero_results"]

    results = {}
    results["l1_norm"] = l1_norm
    results["l2_norm"] = l2_norm
    results["non_zero_results"] = non_zero_results
    results["variables"] = variables
    new_data["Results"] = results
    return new_data


def add_comparison_data_to_point(point_data: dict[str, dict]):
    """Add comparison data to a points results"""
    original_data = point_data[Result.ORIGINAL.name]
    for result in [Result.L1.name, Result.L2.name]:
        if result in point_data.keys():
            l1_norm = calculate_l1_norm(original_data, point_data[result])
            l2_norm = calculate_l2_norm(original_data, point_data[result])
            point_data[result]["l1_norm"] = l1_norm
            point_data[result]["l2_norm"] = l2_norm
            non_zero_results = count_non_zeroes_in_result(
                original_data, point_data[result])
            point_data[result]["non_zero_results"] = non_zero_results


def calculate_l1_norm(
    original: dict[str, float],
    new: dict[str, float],
) -> float:
    """Calculate the l1 norm between original and new point data."""
    return np.sum(
        np.abs([
            original["x"] - new["x"],
            original["y"] - new["y"],
        ]))


def calculate_l2_norm(
    original: dict[str, float],
    new: dict[str, float],
) -> float:
    """Calculate the l2_norm between original and new point data."""
    return np.sum(
        np.square([
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
                            timestamp: datetime = datetime.now(),
                            counter: int = 0) -> Path:
    """Writes data to a json file."""
    time_str = timestamp.strftime("%Y-%m-%dT%H%M")
    filename = time_str + f"--{counter}" + ".json"
    filepath = path / filename
    with open(filepath, "w", encoding="utf8") as file:
        json_string = json.dumps(data, indent=2)
        file.write(json_string)

    return filepath


def read_sketch_from_json_data(
    file_path: Path
) -> tuple[dict[str, tuple[float]], dict[str, list[str]], dict[str, dict],
           dict[str, dict]]:
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

        move_dict = {}
        if "moves" in json_data.keys():
            move_dict = json_data["moves"]

        return (points, lines, constraint_dict, move_dict)


def read_results(file_path: Path) -> dict[str, dict]:
    """Read the results in to a dictionary."""
    with open(file_path, "r", encoding="utf8") as file:
        json_data = json.load(file)
        results = {}
        if "Results" in json_data.keys():
            results = json_data["Results"]

    return results


def read_points_to_latex_table(file_path: Path,
                               is_printing: bool) -> list[str]:
    """Read the points in to a latex table."""
    # $P_{10}(x,y)$ & (1.929, -0.623) & (1.786, -0.332) & (1.709, -0.415)\\
    with open(file_path, "r", encoding="utf8") as file:
        json_data = json.load(file)
        points = []
        if "points" in json_data.keys():
            points_data = json_data["points"]
            point_count = 1
            for key in points_data.keys():
                point_str = f"$P_{{{point_count}}}(x,y)$"
                pnt = points_data[key]
                for result in pnt.keys():
                    x = points_data[key][result]["x"]
                    y = points_data[key][result]["y"]
                    point_str = point_str + f" & ({x:.3f}, {y:.3f})"

                point_str = point_str + "\\\\"
                points.append(point_str)
                point_count += 1

        if is_printing:
            for pnt_str in points:
                print(pnt_str)

    return points


def read_results_to_latex_table(file_path: Path,
                                is_printing: bool) -> list[str]:
    """Read the results in to a latex table."""
    # L1 & 0.0007 & 1 & 1.5 & 2.25 & 1\\
    with open(file_path, "r", encoding="utf8") as file:
        json_data = json.load(file)
        results = []
        order = ["time", "steps", "l1_norm", "l2_norm", "non_zero_results"]
        if "Results" in json_data.keys():
            result_data = json_data["Results"]
            for result in [Result.L1, Result.L2]:
                result_str = f"{result.name}"
                for key in order:
                    data = result_data[key][result.name]
                    if key == "time":
                        res = f"{data:.5f}"
                    elif key in ["l1_norm", "l2_norm"]:
                        res = f"{data:.3f}"
                    else:
                        res = f"{data}"
                    result_str = result_str + " & " + res
                result_str = result_str + "\\\\"
                results.append(result_str)
        if is_printing:
            for res_str in results:
                print(res_str)

    return results


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
                            points_dict: dict[str, tuple[float]],
                            constraint_dict: dict[str, dict],
                            move_dict: dict[str, dict],
                            json_path: Path,
                            counter: int = 0,
                            plot_data: bool = False):
    """Creates an adjacent sketch and solves it."""
    json_data = {}
    if plot_data:
        fig, axes = plt.subplots(1, 3, sharex='row', sharey='row')
        fig.canvas.draw()
    subplot_int = 0
    l1_time = 0.0
    l2_time = 0.0
    l1_steps = 0
    l2_steps = 0

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
            json_data["moves"] = move_dict
            if plot_data:
                ax = axes[subplot_int]
                ax.set_title("Original")
                add_lines_to_plot(ax, lines, constraint_dict)
                add_points_to_plot(ax, points)
                add_circles_to_plot(ax, circles)
                # add_annotations_for_angle_constraints(ax, lines, constraint_dict)
                subplot_int += 1

        s = Sketch()
        for line in lines.values():
            s.add_entity(line)

        for cc in circles.values():
            s.add_entity(cc)

        for constraint in constraint_list:
            s.add_constraint(constraint)

        # And solve!
        if result == Result.L1:
            s.use_linear_program(True)
        else:
            s.use_linear_program(False)

        for key in move_dict.keys():
            new_point = point(key, move_dict[key]["values"])
            old_point = points[move_dict[key]["point"]]
            move_expression = old_point.drag_to(new_point.expr())
            s.add_expressionVector(move_expression)

        t1_start = time()
        steps = s.update()
        t1_stop = time()

        if result == Result.L1:
            l1_time = t1_stop - t1_start
            l1_steps = steps
        else:
            l2_time = t1_stop - t1_start
            l2_steps = steps

        if plot_data:
            ax2 = axes[subplot_int]
            ax2.set_title(f"{result.name}")
            add_lines_to_plot(ax2, lines, constraint_dict)
            add_points_to_plot(ax2, points)
            add_circles_to_plot(ax2, circles)
            # add_annotations_for_angle_constraints(ax2, lines, constraint_dict)
            subplot_int += 1

        json_data = export_entities_to_dict(points=points,
                                            data=json_data,
                                            result=result)

    json_data = add_comparison_data(json_data)
    json_data["Results"]["time"] = {}
    json_data["Results"]["time"]["L1"] = l1_time
    json_data["Results"]["time"]["L2"] = l2_time
    json_data["Results"]["steps"] = {}
    json_data["Results"]["steps"]["L1"] = l1_steps
    json_data["Results"]["steps"]["L2"] = l2_steps
    file_path = write_data_to_json_file(path=json_path,
                                        data=json_data,
                                        counter=counter)
    # plt.legend()
    # plt.show()

    return file_path
