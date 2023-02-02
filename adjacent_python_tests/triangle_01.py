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

# points["p1"] = (2.0, 1.0)
# points["p2"] = (6.0, 1.0)
# points["p3"] = (4.17964055775109, 1.8284271247461896)

lines = {}
lines["l1"] = ["p1", "p2"]
lines["l2"] = ["p2", "p3"]
lines["l3"] = ["p3", "p1"]

A = 4
B = 2
C = np.sqrt(np.sum(np.square([A, B])))

constraint_dict = {}
# constraint_dict["c1"] = {
#     "type": PyConstraints.LENGTH,
#     "entities": ["l1"],
#     "value": A
# }

# constraint_dict["c2"] = {
#     "type": PyConstraints.LENGTH,
#     "entities": ["l2"],
#     "value": B
# }

# constraint_dict["c3"] = {
#     "type": PyConstraints.LENGTH,
#     "entities": ["l3"],
#     "value": C
# }

constraint_dict["c4"] = {
    "type": PyConstraints.ORTHOGONAL,
    "entities": ["l1", "l2"],
}

move_dict = {}
move_dict["m1"] = {"point": "p3", "values": (5, 2)}

create_and_solve_sketch(lines_dict=lines,
                        circle_dict={},
                        points_dict=points,
                        constraint_dict=constraint_dict,
                        move_dict=move_dict,
                        json_path=Path("/home/nathan/Downloads/Books"))
