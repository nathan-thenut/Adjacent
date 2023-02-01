from pathlib import Path
from utils import (read_sketch_from_json_data, create_and_solve_sketch,
                   read_results, Result)

file = Path(
    "/home/nathan/Uni-Stuff/CG/Adjacent/data/pentagon/01/2023-01-19T1252.json")

(points, lines, constraint_dict) = read_sketch_from_json_data(file)

# points = read_results(file, Result.L1, True)

print(points)
print(lines)
print(constraint_dict)

create_and_solve_sketch(lines_dict=lines,
                        circle_dict={},
                        points_dict=points,
                        constraint_dict=constraint_dict,
                        json_path=Path("/home/nathan/Downloads/Books"))
