import numpy as np

# 0-D array (scalar)
a = np.array(42)

# 1-D array (vector)
b = np.array([1, 2, 3, 4, 5])

# 2-D array (matrix)
c = np.array([[1, 2, 3], [4, 5, 6]])

# 3-D array (tensor)
d = np.array([[[1, 2, 3], [4, 5, 6]], [[1, 2, 3], [4, 5, 6]]])

# custom dimensions
arr = np.array([1, 2, 3, 4], ndmin=5)

print(a.ndim, "dimension")
print(b.ndim, "dimension")
print(c.ndim, "dimension")
print(d.ndim, "dimension")
print(arr, 'number of dimensions :', arr.ndim)