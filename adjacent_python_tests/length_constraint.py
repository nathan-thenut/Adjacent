import matplotlib.pyplot as plt
from adjacent_api import *
from utils import point, add_lines_to_plot

p1 = point("p1", (0, 1, 0))
p2 = point("p2", (4, 1, 0))
p3 = point("p3", (1, 3, 0))
p4 = point("p4", (2, 0, 0))

l1 = Line(p1, p2)
l2 = Line(p3, p4)

fig = plt.figure()
ax = fig.add_subplot(121, projection='3d')
ax.set_title("Before")
lines = {}
lines["l1"] = l1
lines["l2"] = l2

add_lines_to_plot(ax, lines)

s = Sketch()

s.add_entity(l1)
s.add_entity(l2)

s.add_constraint(constraints.Length(l1, 4))
s.add_constraint(constraints.Length(l2, 4))
# And solve!
s.update()

ax2 = fig.add_subplot(122, projection='3d')
ax2.set_title("After")
add_lines_to_plot(ax2, lines)

plt.legend()
plt.show()

print("L1: ", l1)
print("L2: ", l2)
