import numpy as np
from pathlib import Path
from utils import (
    PyConstraints,
    create_and_solve_sketch,
)

points = {}
points["p1"] = (0, 1)
points["p2"] = (4, 1)
points["p3"] = (4, 3)
points["p4"] = (0, 3)

points["p5"] = (4, 4)

lines = {}
lines["l1"] = ["p1", "p2"]
lines["l2"] = ["p2", "p3"]
lines["l3"] = ["p3", "p1"]
lines["l4"] = ["p2", "p4"]

ANGLE = np.deg2rad(60)
A = 4
B = 2
C = np.sqrt(np.sum(np.square([A, B])))

constraint_dict = {}
# constraint_dict["c1"] = {
#     "type": PyConstraints.LENGTH,
#     "entities": ["l1"],
#     "value": A
# }
#
# constraint_dict["c2"] = {
#     "type": PyConstraints.LENGTH,
#     "entities": ["l2"],
#     "value": B
# }
#
constraint_dict["c3"] = {
    "type": PyConstraints.LENGTH,
    "entities": ["l4"],
    "value": 2
}

#
# constraint_dict["c5"] = {
#     "type": PyConstraints.ANGLE,
#     "entities": ["l4", "l1"],
#     "value": -ANGLE / 2
# }

constraint_dict["c4"] = {
    "type": PyConstraints.ANGLE,
    "entities": ["l2", "l1"],
    "value": -ANGLE
}

constraint_dict["c5"] = {
    "type": PyConstraints.ANGLE,
    "entities": ["l2", "l4"],
    "value": ANGLE / 2
}

# constraint_dict["c6"] = {
#     "type": PyConstraints.POINTON,
#     "entities": ["p3", "p5"],
# }

create_and_solve_sketch(
    lines_dict=lines,
    points_dict=points,
    circle_dict={},
    constraint_dict=constraint_dict,
    json_path=Path("/home/nathan/Uni-Stuff/CG/Adjacent/data/triangle/02/"))
