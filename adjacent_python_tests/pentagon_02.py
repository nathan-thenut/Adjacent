import random
import numpy as np
from pathlib import Path
from core_utils import (PyConstraints, create_and_solve_sketch,
                        generate_vectors_with_distance)

offset_pairs = generate_vectors_with_distance(1, count=30)
for i in range(len(offset_pairs)):
    points = {}
    points["p1"] = (0.039, 0.02701158784136345)
    points["p2"] = (0.0968479252882644, 3.263)
    points["p3"] = (3.1337363070211173, 0.972)
    points["p4"] = (1.893, -2.6230575905296067)
    points["p5"] = (-1.909, -2.5532955256185668)
    points["p6"] = (-3.019, 1.0824264121634164)

    points["p7"] = (0.06792396264413221, 1.6450057939206817)
    points["p8"] = (1.2430000808939146, 1.6239996261479137)
    points["p9"] = (1.5863681535105587, 0.49950579392068173)
    points["p10"] = (1.9294345225255194, -0.6239999911748865)
    points["p11"] = (0.966, -1.2980230013441214)
    points["p12"] = (0.0033148641860392615, -1.9715217372889065)
    points["p13"] = (-0.935, -1.2631419688886016)
    points["p14"] = (-1.872999944258877, -0.5549999489388252)
    points["p15"] = (-1.490, 0.5547190000023899)
    points["p16"] = (-1.1064610767450938, 1.6659996076695156)

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

    # constraint_dict["c1"] = {
    #     "type": PyConstraints.ANGLE,
    #     "entities": ["l1", "l2"],
    #     "value": -ANGLE
    # }
    #
    # constraint_dict["c2"] = {
    #     "type": PyConstraints.ANGLE,
    #     "entities": ["l2", "l3"],
    #     "value": -ANGLE
    # }
    #
    # constraint_dict["c3"] = {
    #     "type": PyConstraints.ANGLE,
    #     "entities": ["l3", "l4"],
    #     "value": -ANGLE
    # }
    #
    # constraint_dict["c4"] = {
    #     "type": PyConstraints.ANGLE,
    #     "entities": ["l4", "l5"],
    #     "value": -ANGLE
    # }
    #
    # constraint_dict["c5"] = {
    #     "type": PyConstraints.ANGLE,
    #     "entities": ["l5", "l1"],
    #     "value": -ANGLE
    # }

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

    # constraint_dict["c21"] = {
    #     "type": PyConstraints.EQUAL,
    #     "entities": ["l6", "l7"]
    # }
    #
    # constraint_dict["c22"] = {
    #     "type": PyConstraints.EQUAL,
    #     "entities": ["l6", "l8"]
    # }
    #
    # constraint_dict["c23"] = {
    #     "type": PyConstraints.EQUAL,
    #     "entities": ["l6", "l9"]
    # }
    #
    # constraint_dict["c24"] = {
    #     "type": PyConstraints.EQUAL,
    #     "entities": ["l6", "l10"]
    # }
    movable_points_names = [
        "p1", "p7", "p8", "p9", "p10", "p11", "p12", "p13", "p14", "p15", "p16"
    ]
    movable_points = {}
    for key in movable_points_names:
        movable_points[key] = points[key]
    selected_point, selected_values = random.choice(
        list(movable_points.items()))
    xoffset = offset_pairs[i][0]
    yoffset = offset_pairs[i][1]
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
