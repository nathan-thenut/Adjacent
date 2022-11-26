import matplotlib.pyplot as plt

figure, axes = plt.subplots()
p1 = (0.5, 0.5)
cc = plt.Circle(p1, 0.4, fill=False, in_layout=True)
axes.add_patch(cc)
axes.scatter(p1[0], p1[1])
axes.set_aspect("equal", adjustable="datalim")
axes.set_box_aspect(0.5)
axes.autoscale()
plt.title('Colored Circle')
plt.show()
