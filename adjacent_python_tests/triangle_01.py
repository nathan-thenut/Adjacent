import random
from pathlib import Path
from core_utils import (
    PyConstraints,
    create_and_solve_sketch,
)

for i in range(100):
    points = {}
    points["p1"] = (0, 1)
    points["p2"] = (4, 1)
    points["p3"] = (4, 3)

    lines = {}
    lines["l1"] = ["p1", "p2"]
    lines["l2"] = ["p2", "p3"]
    lines["l3"] = ["p3", "p1"]

    A = 4

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

    offset_choices = [1, -1]

    selected_point, selected_values = random.choice(list(points.items()))
    xoffset = random.choice(offset_choices)
    yoffset = random.choice(offset_choices)
    new_values = (selected_values[0] + xoffset, selected_values[1] + yoffset)
    move_dict = {}
    move_dict["m1"] = {"point": selected_point, "values": new_values}

    create_and_solve_sketch(
        lines_dict=lines,
        circle_dict={},
        points_dict=points,
        constraint_dict=constraint_dict,
        move_dict=move_dict,
        json_path=Path("/home/nathan/Downloads/Books/triangle-01/"),
        counter=i)
