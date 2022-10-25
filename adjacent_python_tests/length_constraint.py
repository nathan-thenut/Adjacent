import matplotlib.pyplot as plt
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

for result in [Result.L1, Result.L2]:

    p1 = point("p1", (0, 1))
    p2 = point("p2", (4, 1))
    p3 = point("p3", (1, 3))
    p4 = point("p4", (2, 0))

    l1 = Line(p1, p2)
    l2 = Line(p3, p4)

    fig = plt.figure()
    ax = fig.add_subplot(121)
    ax.set_title("Before")
    lines = {}
    lines["l1"] = l1
    lines["l2"] = l2

    if not json_data:
        json_data = export_entities_to_dict(lines=lines)

    add_lines_to_plot(ax, lines)

    s = Sketch()

    s.add_entity(l1)
    s.add_entity(l2)

    s.add_constraint(constraints.Length(l1, 6))
    s.add_constraint(constraints.Length(l2, 6))
    s.add_constraint(constraints.Orthogonal(l1, l2))
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

write_data_to_json_file(path=Path("/tmp/"), data=json_data)
