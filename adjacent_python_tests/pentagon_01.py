import random
import gc
from pathlib import Path
import numpy as np
from core_utils import (PyConstraints, create_and_solve_sketch,
                        generate_vectors_with_distance)

offset_pairs = generate_vectors_with_distance(1, count=100)
for i, pair in enumerate(offset_pairs):
    points = {}
    points["p1"] = (0.6156184929834163, 0.08539832151226268)
    points["p2"] = (1.0189514043843646, 3.173)
    points["p3"] = (2.99, 0.52793350909513)
    points["p4"] = (2.031995020634442, -2.517)
    points["p5"] = (-1.8489975458714059, -2.517)
    points["p6"] = (-3.0, 1.8055)

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

    # constraint_dict["c3"] = {
    #     "type": PyConstraints.ANGLE,
    #     "entities": ["l3", "l4"],
    #     "value": -ANGLE
    # }

    # constraint_dict["c4"] = {
    #     "type": PyConstraints.ANGLE,
    #     "entities": ["l4", "l5"],
    #     "value": -ANGLE
    # }

    # constraint_dict["c5"] = {
    #     "type": PyConstraints.ANGLE,
    #     "entities": ["l5", "l1"],
    #     "value": -ANGLE
    # }

    # constraint_dict["c6"] = {"type": PyConstraints.EQUAL, "entities": ["l6", "l7"]}
    #
    # constraint_dict["c7"] = {"type": PyConstraints.EQUAL, "entities": ["l6", "l8"]}
    #
    # constraint_dict["c8"] = {"type": PyConstraints.EQUAL, "entities": ["l6", "l9"]}
    #
    # constraint_dict["c9"] = {
    #     "type": PyConstraints.EQUAL,
    #     "entities": ["l6", "l10"]
    # }
    #

    selected_point = random.choice(list(points.keys())[:4])
    selected_values = points[selected_point]
    xoffset = pair[0]
    yoffset = pair[1]
    new_values = (selected_values[0] + xoffset, selected_values[1] + yoffset)

    move_dict = {}
    move_dict["m1"] = {"point": selected_point, "values": new_values}

    create_and_solve_sketch(lines_dict=lines,
                            circle_dict={},
                            points_dict=points,
                            constraint_dict=constraint_dict,
                            move_dict=move_dict,
                            json_path=Path("/home/nathan/Downloads/Books"),
                            counter=i)
    gc.collect()
