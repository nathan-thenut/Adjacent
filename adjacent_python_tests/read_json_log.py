from pathlib import Path
from utils import read_sketch_from_json_data, create_and_solve_sketch

file = Path(
    "/home/nathan/Uni-Stuff/CG/Adjacent/data/triangle/01/2022-11-23T2020.json")

(points, lines, constraint_dict) = read_sketch_from_json_data(file)

print(points)
print(lines)
print(constraint_dict)

create_and_solve_sketch(lines_dict=lines,
                        circle_dict={},
                        points_dict=points,
                        constraint_dict=constraint_dict,
                        json_path=Path("/tmp/"))
