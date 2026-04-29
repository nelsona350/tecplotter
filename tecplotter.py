import numpy as np
import matplotlib.pyplot as plt

I, J, K = 31, 49, 1
n = I * J * K

with open("for022.dat") as f:
    lines = f.readlines()

# Skip first two header lines
nums = np.fromstring(" ".join(lines[2:]), sep=" ")

X = nums[0:n]
Y = nums[n : 2 * n]
Z = nums[2 * n : 3 * n]

X = X.reshape((J, I))
Y = Y.reshape((J, I))
Z = Z.reshape((J, I))

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
ax.plot_surface(X, Y, Z, cmap="viridis", edgecolor="none")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.set_title("3D Surface Plot of Loaded X, Y, Z")
plt.show()
