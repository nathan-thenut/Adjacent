import numpy as np
import pprint
from pathlib import Path
from utils import (PyConstraints, create_and_solve_sketch)

pp = pprint.PrettyPrinter(indent=2)

POINT_COUNT = 100

x_values = np.random.randint(low=-20, high=20, size=POINT_COUNT)
y_values = np.random.randint(low=-20, high=20, size=POINT_COUNT)

points = {}
for i in range(POINT_COUNT):
    points[f"p{i}"] = (x_values[i], y_values[i])

lines = {}
line_count = 0
for i in range(0, POINT_COUNT, 2):
    lines[f"l{line_count}"] = [f"p{i}", f"p{i + 1}"]
    line_count += 1

constraint_dict = {}
for i in range(0, line_count):
    constraint_dict[f"c{i}"] = {
        "type": PyConstraints.LENGTH,
        "entities": [f"l{i}"],
        "value": 6
    }

constraint_count = len(constraint_dict.keys())
for i in range(0, (line_count - 1), 2):
    constraint_dict[f"c{constraint_count}"] = {
        "type": PyConstraints.ORTHOGONAL,
        "entities": [f"l{i}", f"l{i+1}"],
    }
    constraint_count += 1

# pp.pprint(constraint_dict)
create_and_solve_sketch(lines_dict=lines,
                        points_dict=points,
                        constraint_dict=constraint_dict,
                        json_path=Path("/home/nathan/Downloads/Books"))
