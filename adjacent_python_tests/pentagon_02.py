import numpy as np
from pathlib import Path
from utils import (
    PyConstraints,
    create_and_solve_sketch,
)

points = {}
points["p1"] = (0, 0)
points["p2"] = (0, 3)
points["p3"] = (3, 1)
points["p4"] = (3, -1)
points["p5"] = (-3, -1)
points["p6"] = (-3, 1)

points["p7"] = (0.1, 1.5)
points["p8"] = (0.2, 1.5)
points["p9"] = (1.5, 0.75)
points["p10"] = (1.5, 0.0)
points["p11"] = (1.5, -0.1)
points["p12"] = (0, -0.5)
points["p13"] = (-1.5, -0.5)
points["p14"] = (-2, 0.0)
points["p15"] = (-2, 0.5)
points["p16"] = (-1.5, 1.5)

points["p17"] = (2, 4)

lines = {}
lines["l1"] = ["p1", "p2"]
lines["l2"] = ["p1", "p3"]
lines["l3"] = ["p1", "p4"]
lines["l4"] = ["p1", "p5"]
lines["l5"] = ["p1", "p6"]

lines["l6"] = ["p2", "p3"]
lines["l7"] = ["p3", "p4"]
lines["l8"] = ["p4", "p5"]
lines["l9"] = ["p5", "p6"]
lines["l10"] = ["p6", "p2"]

lines["l11"] = ["p7", "p8"]
lines["l12"] = ["p8", "p9"]
lines["l13"] = ["p9", "p10"]
lines["l14"] = ["p10", "p11"]
lines["l15"] = ["p11", "p12"]
lines["l16"] = ["p12", "p13"]
lines["l17"] = ["p13", "p14"]
lines["l18"] = ["p14", "p15"]
lines["l19"] = ["p15", "p16"]
lines["l20"] = ["p16", "p7"]

ANGLE = np.deg2rad(72)

constraint_dict = {}

constraint_dict["c1"] = {
    "type": PyConstraints.ANGLE,
    "entities": ["l1", "l2"],
    "value": -ANGLE
}

constraint_dict["c2"] = {
    "type": PyConstraints.ANGLE,
    "entities": ["l2", "l3"],
    "value": -ANGLE
}

constraint_dict["c3"] = {
    "type": PyConstraints.ANGLE,
    "entities": ["l3", "l4"],
    "value": -ANGLE
}

constraint_dict["c4"] = {
    "type": PyConstraints.ANGLE,
    "entities": ["l4", "l5"],
    "value": -ANGLE
}

constraint_dict["c5"] = {
    "type": PyConstraints.ANGLE,
    "entities": ["l5", "l1"],
    "value": -ANGLE
}

constraint_dict["c6"] = {
    "type": PyConstraints.MIDPOINT,
    "entities": ["p1", "p2", "p7"],
}

constraint_dict["c7"] = {
    "type": PyConstraints.MIDPOINT,
    "entities": ["p1", "p3", "p9"],
}

constraint_dict["c8"] = {
    "type": PyConstraints.ORTHOGONAL,
    "entities": ["l1", "l11"],
}

constraint_dict["c9"] = {
    "type": PyConstraints.ORTHOGONAL,
    "entities": ["l2", "l12"],
}

constraint_dict["c10"] = {
    "type": PyConstraints.MIDPOINT,
    "entities": ["p1", "p4", "p11"],
}

constraint_dict["c11"] = {
    "type": PyConstraints.ORTHOGONAL,
    "entities": ["l2", "l13"],
}

constraint_dict["c12"] = {
    "type": PyConstraints.ORTHOGONAL,
    "entities": ["l3", "l14"],
}

constraint_dict["c13"] = {
    "type": PyConstraints.MIDPOINT,
    "entities": ["p1", "p5", "p13"],
}

constraint_dict["c14"] = {
    "type": PyConstraints.ORTHOGONAL,
    "entities": ["l3", "l15"],
}

constraint_dict["c15"] = {
    "type": PyConstraints.ORTHOGONAL,
    "entities": ["l4", "l16"],
}

constraint_dict["c16"] = {
    "type": PyConstraints.MIDPOINT,
    "entities": ["p1", "p6", "p15"],
}

constraint_dict["c17"] = {
    "type": PyConstraints.ORTHOGONAL,
    "entities": ["l4", "l17"],
}

constraint_dict["c18"] = {
    "type": PyConstraints.ORTHOGONAL,
    "entities": ["l5", "l18"],
}

constraint_dict["c19"] = {
    "type": PyConstraints.ORTHOGONAL,
    "entities": ["l5", "l19"],
}

constraint_dict["c20"] = {
    "type": PyConstraints.ORTHOGONAL,
    "entities": ["l1", "l20"],
}

constraint_dict["c21"] = {
    "type": PyConstraints.EQUAL,
    "entities": ["l6", "l7"]
}

constraint_dict["c22"] = {
    "type": PyConstraints.EQUAL,
    "entities": ["l6", "l8"]
}

constraint_dict["c23"] = {
    "type": PyConstraints.EQUAL,
    "entities": ["l6", "l9"]
}

constraint_dict["c24"] = {
    "type": PyConstraints.EQUAL,
    "entities": ["l6", "l10"]
}

constraint_dict["c25"] = {
    "type": PyConstraints.POINTON,
    "entities": ["p1", "p17"],
}

create_and_solve_sketch(lines_dict=lines,
                        circle_dict={},
                        points_dict=points,
                        constraint_dict=constraint_dict,
                        json_path=Path("/home/nathan/Downloads/Books"))
