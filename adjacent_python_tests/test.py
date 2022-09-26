from adjacent_api import *
import math

# Adjacent computes everything symbolically so we need to create named parameters

x = Param("x", 0.0)
y = Param("y", 5.0)
z = Param("z", 1.0)

# Now we can create a point at (0, 5, 1)
p1 = Point(x, y, z)


# helper function
def point(name, xyz=(0, 0, 0)):
    if len(xyz) <= 2:
        xyz = (*xyz, 0)
    return Point(Param(f"{name}_x", xyz[0]), Param(f"{name}_y", xyz[1]),
                 Param(f"{name}_z", xyz[2]))


p2 = point("p2", (3, 1, 2))
p3 = point("p3", (5, 5, 9))
p4 = point("p4", (1, 2, 9))
p5 = point("cc1", (1, 1))

p6 = point("p6", (0, 1, 0))
p7 = point("p7", (4, 1, 0))

p8 = point("p8", (2, 3, 0))
p9 = point("p9", (2, 0, 0))

l1 = Line(p1, p2)
l2 = Line(p3, p4)
c1 = Circle(p5, Param("rad1", 1.2))

l3 = Line(p6, p7)
l4 = Line(p8, p9)

s = Sketch()

s.add_entity(l1)
s.add_entity(l2)
s.add_entity(c1)

s.add_entity(l3)
s.add_entity(l4)

DESIRED_ANGLE = -0.8 * math.pi

# Let's add some constraints to the sketch
s.add_constraint(constraints.Coincident(p2, p4))
s.add_constraint(constraints.Diameter(c1, 2.5))

s.add_constraint(constraints.Coincident(p1, p5))
# s.add_constraint(constraints.Tangent(c1, l1))

s.add_constraint(constraints.Length(l1, 5))
s.add_constraint(constraints.Length(l2, 1.5))

# Horizontal / Vertical constraint
s.add_constraint(constraints.HV(l1, constraints.HVOrientation.OY))

# s.add_constraint(constraints.HV(l2, constraints.HVOrientation.OY))
s.add_constraint(constraints.Angle(l1, l2, DESIRED_ANGLE))
# s.add_constraint(constraints.Parallel(l1, l2))
# s.add_constraint(constraints.HV(l1, constraints.HVOrientation.OX))
# s.add_constraint(constraints.Length(l2, 1.5))
# s.add_constraint(constraints.Distance(p2, p3, 0.5))
# s.add_constraint(constraints.PointOn(p3, l1))
s.add_constraint(constraints.Length(l3, 4))
s.add_constraint(constraints.Length(l4, 4))
s.add_constraint(constraints.Orthogonal(l3, l4))
# And solve!
s.update()

print("L1: ", l1)
print("L2: ", l2)
print("C1: ", c1)
print("L3: ", l3)
print("L4: ", l4)
