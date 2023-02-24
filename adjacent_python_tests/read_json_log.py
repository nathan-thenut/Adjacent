from pathlib import Path
from core_utils import (read_sketch_from_json_data, create_and_solve_sketch,
                        read_results, read_results_to_latex_table, Result)

file = Path(
    "/home/nathan/Uni-Stuff/CG/Adjacent/data/triangle/01/single_run/2023-02-24T2307--0.json"
)

# (points, lines, constraint_dict, move_dict) = read_sketch_from_json_data(file)

# points = read_results(file, Result.L1, True)
print(file.stem)
read_results_to_latex_table(file, True)

# print(points)
# print(lines)
# print(constraint_dict)
# print(move_dict)

# create_and_solve_sketch(lines_dict=lines,
#                         circle_dict={},
#                         points_dict=points,
#                         constraint_dict=constraint_dict,
#                         move_dict=move_dict,
#                         json_path=Path("/home/nathan/Downloads/Books"),
#                         plot_data=True)
