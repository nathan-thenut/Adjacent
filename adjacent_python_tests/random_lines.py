import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from adjacent_api import *
from utils import (
    point,
    add_lines_to_plot,
    export_entities_to_dict,
    write_data_to_json_file,
    add_comparison_data,
    Result,
)

json_data = {}

x_values = np.random.randint(low=-10, high=10, size=10)
y_values = np.random.randint(low=-10, high=10, size=10)

for result in [Result.L1, Result.L2]:

    points = []
    for i in range(10):
        points.append(point(f"p{i}", (x_values[i], y_values[i])))

    lines = {}
    line_count = 0
    for i in range(0, 10, 2):
        lines[f"l{line_count}"] = Line(points[i], points[i + 1])
        line_count += 1

    if not json_data:
        json_data = export_entities_to_dict(lines=lines)

    fig = plt.figure()
    ax = fig.add_subplot(121)
    ax.set_title("Before")
    add_lines_to_plot(ax, lines)

    s = Sketch()

    for line in lines.values():
        s.add_entity(line)

    range_max = line_count
    if range_max % 2 > 0:
        range_max -= 1
    for line in lines.values():
        s.add_constraint(constraints.Length(line, 5))

    # And solve!
    if result == Result.L1:
        s.use_linear_program(True)
    else:
        s.use_linear_program(False)
    s.update()

    ax2 = fig.add_subplot(122)
    ax2.set_title("After")
    add_lines_to_plot(ax2, lines)

    plt.legend()
    plt.show()

    json_data = export_entities_to_dict(lines=lines,
                                        data=json_data,
                                        result=result)
json_data = add_comparison_data(json_data)

write_data_to_json_file(path=Path("/home/nathan/Downloads/Books"),
                        data=json_data)
