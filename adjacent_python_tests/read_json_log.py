from pathlib import Path
from utils import read_sketch_from_json_data

file = Path("/home/nathan/Downloads/Books/2022-10-31T1957.json")

(points, lines, constraint_dict) = read_sketch_from_json_data(file)

print(points)
print(lines)
print(constraint_dict)
