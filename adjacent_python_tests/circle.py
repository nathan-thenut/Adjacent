import numpy as np
from pathlib import Path
from utils import PyConstraints, create_and_solve_sketch

points = {}
points["p1"] = (0, 0)
points["p2"] = (1, 1)

lines = {}
circles = {}

circles["c1"] = ("p1", 2)

constraint_dict = {}

constraint_dict["c1"] = {
    "type": PyConstraints.POINTON,
    "entities": ["p1", "p2"],
}

log_path = create_and_solve_sketch(
    lines_dict=lines,
    circle_dict=circles,
    points_dict=points,
    constraint_dict=constraint_dict,
    json_path=Path("/home/nathan/Downloads/Books"))
