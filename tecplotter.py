import numpy as np

I, J, K = 31, 49, 1
n = I * J * K

with open("for022.dat") as f:
    lines = f.readlines()

# Skip first two header lines
nums = np.fromstring(" ".join(lines[2:]), sep=' ')

X = nums[0:n]
Y = nums[n:2*n]
Z = nums[2*n:3*n]

X = X.reshape((J, I))
Y = Y.reshape((J, I))
Z = Z.reshape((J, I))