from pathlib import Path
from utils import (
    PyConstraints,
    create_and_solve_sketch,
)

points = {}
points["p1"] = (0, 1)
points["p2"] = (4, 1)
points["p3"] = (4, 5)
points["p4"] = (0, 5)

points["p5"] = (4, 8)

lines = {}
lines["l1"] = ["p1", "p2"]
lines["l2"] = ["p2", "p3"]
lines["l3"] = ["p3", "p4"]
lines["l4"] = ["p4", "p1"]

constraint_dict = {}
# constraint_dict["c0"] = {
#     "type": PyConstraints.LENGTH,
#     "entities": ["l1"],
#     "value": 4
# }
#
# constraint_dict["c1"] = {
#     "type": PyConstraints.LENGTH,
#     "entities": ["l2"],
#     "value": 4
# }
#
# constraint_dict["c2"] = {
#     "type": PyConstraints.LENGTH,
#     "entities": ["l3"],
#     "value": 4
# }
#
# constraint_dict["c3"] = {
#     "type": PyConstraints.LENGTH,
#     "entities": ["l4"],
#     "value": 4
# }

constraint_dict["c3"] = {
    "type": PyConstraints.EQUAL,
    "entities": ["l1", "l2"],
}

constraint_dict["c4"] = {
    "type": PyConstraints.ORTHOGONAL,
    "entities": ["l1", "l2"],
}

constraint_dict["c5"] = {
    "type": PyConstraints.ORTHOGONAL,
    "entities": ["l2", "l3"],
}

constraint_dict["c6"] = {
    "type": PyConstraints.ORTHOGONAL,
    "entities": ["l3", "l4"],
}

constraint_dict["c6"] = {
    "type": PyConstraints.ORTHOGONAL,
    "entities": ["l4", "l1"],
}

# constraint_dict["c7"] = {
#     "type": PyConstraints.POINTON,
#     "entities": ["p3", "p5"],
# }

create_and_solve_sketch(lines_dict=lines,
                        points_dict=points,
                        constraint_dict=constraint_dict,
                        json_path=Path("/home/nathan/Downloads/Books"))
