import numpy as np
from pathlib import Path
from utils import PyConstraints, create_and_solve_sketch

points = {}
points["p1"] = (0, 0)
points["p2"] = (1, 0)
points["p3"] = (1, 1)

lines = {}
lines["l1"] = ["p1", "p2"]
lines["l2"] = ["p2", "p3"]

ANGLE = np.deg2rad(80)

constraint_dict = {}

constraint_dict["c1"] = {
    "type": PyConstraints.ANGLE,
    "entities": ["l1", "l2"],
    "value": ANGLE
}

log_path = create_and_solve_sketch(
    lines_dict=lines,
    points_dict=points,
    circle_dict={},
    constraint_dict=constraint_dict,
    json_path=Path("/home/nathan/Downloads/Books"))
