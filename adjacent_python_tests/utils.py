from adjacent_api import *


# helper function
def point(name, xyz=(0, 0, 0)):
    """Creates a point using Adjacent's point entity."""
    if len(xyz) <= 2:
        xyz = (*xyz, 0)
    return Point(Param(f"{name}_x", xyz[0]), Param(f"{name}_y", xyz[1]),
                 Param(f"{name}_z", xyz[2]))


def add_lines_to_plot(figure_or_ax,
                      lines: dict[str, Line],
                      three_d: bool = False):
    """Adds Lines from Adjacent to a matplotlib plot."""
    for key in lines.keys():
        l_x = [lines[key].source().x(), lines[key].target().x()]
        l_y = [lines[key].source().y(), lines[key].target().y()]
        l_z = [lines[key].source().z(), lines[key].target().z()]

        if three_d:
            figure_or_ax.scatter(l_x, l_y, l_z)
            figure_or_ax.plot(l_x, l_y, l_z, label=key)
        else:
            figure_or_ax.scatter(l_x, l_y)
            figure_or_ax.plot(l_x, l_y, label=key)
