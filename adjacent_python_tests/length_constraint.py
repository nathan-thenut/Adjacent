from pathlib import Path
from utils import (
    PyConstraints,
    create_and_solve_sketch,
)

points = {}
points["p1"] = (0, 1)
points["p2"] = (4, 1)
points["p3"] = (1, 3)
points["p4"] = (2, 0)

lines = {}
lines["l1"] = ["p1", "p2"]
lines["l2"] = ["p3", "p4"]

constraint_dict = {}
constraint_dict["c1"] = {
    "type": PyConstraints.LENGTH,
    "entities": ["l1"],
    "value": 6
}

constraint_dict["c2"] = {
    "type": PyConstraints.LENGTH,
    "entities": ["l2"],
    "value": 6
}

constraint_dict["c3"] = {
    "type": PyConstraints.ORTHOGONAL,
    "entities": ["l1", "l2"],
}

create_and_solve_sketch(lines_dict=lines,
                        points_dict=points,
                        constraint_dict=constraint_dict,
                        json_path=Path("/tmp/"))
