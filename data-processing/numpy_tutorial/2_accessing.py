import numpy as np

# example of accessing elements in a 0-D array
a = np.array(42)
print(a)

# example of accessing elements in a 1-D array
b = np.array([1, 2, 3, 4, 5])
print(b[0])  # first element
print(b[1])  # second element
print(b[-1]) # last element

# example of accessing elements in a 2-D array
c = np.array([[1, 2, 3], [4, 5, 6]])
print(c[0, 0])  # first row, first column
print(c[1, 2])  # second row, third column
print(c[:, 1])  # all rows, second column

# example of accessing elements in a 3-D array
d = np.array([[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]]])
print(d[0, 0, 0])  # first block, first row, first column
print(d[1, 1, 2])  # second block, second row, third column
print(d[:, 0, 1])  # all blocks, first row, second column   
print(d[0, :, :])  # first block, all rows, all columns
print(d[:, 1, :])  # all blocks, second row, all columns

# example of accessing elements in a custom dimension array
arr = np.array([1, 2, 3, 4], ndmin=5)
print(arr[0, 0, 0, 0, 0])   # accessing the only element in a 5-D array
print(arr[0, 0, 0, 0, :])    # accessing all elements in the last dimension
print(arr[0, 0, 0, :, :])     # accessing all elements in the last two dimensions