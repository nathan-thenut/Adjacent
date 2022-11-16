import json
import numpy as np
from numpy.linalg import norm
from pathlib import Path
from utils import (PyConstraints, create_and_solve_sketch,
                   read_sketch_from_json_data)


def get_angle_between_vectors(vector1, vector2) -> float:
    v1_angle_to_x = np.rad2deg(np.arctan2(vector1["x"], vector1["y"]))
    v2_angle_to_x = np.rad2deg(np.arctan2(vector2["x"], vector2["y"]))

    return max(v1_angle_to_x, v2_angle_to_x) - min(v1_angle_to_x,
                                                   v2_angle_to_x)


points = {}
points["p1"] = (0, 0)
points["p2"] = (4, 0)
points["p3"] = (4, 1)

lines = {}
lines["l1"] = ["p1", "p2"]
lines["l2"] = ["p1", "p3"]

ANGLE = np.deg2rad(72)

constraint_dict = {}

constraint_dict["c1"] = {
    "type": PyConstraints.ANGLE,
    "entities": ["l2", "l1"],
    "value": -ANGLE
}

log_path = create_and_solve_sketch(
    lines_dict=lines,
    points_dict=points,
    constraint_dict=constraint_dict,
    json_path=Path("/home/nathan/Downloads/Books"))

original_points = {}
l1_points = {}
l2_points = {}

lines = {}
with open(log_path, "r", encoding="utf8") as file:
    data = json.load(file)
    lines = data["lines"]

for key in lines.keys():
    target_point = lines[key]["points"]["target"]
    original_points[key] = {}
    l1_points[key] = {}
    l2_points[key] = {}
    for result in target_point.keys():
        if result == "ORIGINAL":
            original_points[key] = target_point[result]
        if result == "L1":
            l1_points[key] = target_point[result]
        if result == "L2":
            l2_points[key] = target_point[result]

print(f"Original points: {original_points}")
print(f"l1 points: {l1_points}")
print(f"l2 points: {l2_points}")

original_angle = get_angle_between_vectors(original_points["l1"],
                                           original_points["l2"])

l1_angle = get_angle_between_vectors(l1_points["l1"], l1_points["l2"])
l2_angle = get_angle_between_vectors(l2_points["l1"], l2_points["l2"])
print(f"Original angle: {original_angle}")
print(f"l1 angle: {l1_angle}")
print(f"l2 angle: {l2_angle}")
