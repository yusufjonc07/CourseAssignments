# Slicing and Indexing
import numpy as np
# example of slicing in a 1-D array
a = np.array([1, 2, 3, 4, 5])
print(a[1:4])  # elements from index 1 to 3
print(a[:3])   # elements from start to index 2
print(a[2:])   # elements from index 2 to end
print(a[-3:])  # last three elements
print(a[::2])  # every second element   

# example of slicing in a 2-D array
b = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(b[0:2, 1:3])  # rows 0-1, columns 1-2
print(b[:2, :2])    # first two rows and first two columns
print(b[1:, 1:])    # from row 1 and column 1 to the end 

# example of slicing in a 3-D array
c = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
print(c[0:1, :, :])  # first block
print(c[:, 1, :])    # all blocks, second row
print(c[:, :, 0])    # all blocks, all rows, first column

# example of slicing in a custom dimension array
arr = np.array([1, 2, 3, 4], ndmin=5)
print(arr[0, 0, 0, 0, :])    # accessing all elements in the last dimension
print(arr[0, 0, 0, :, :])     # accessing all elements in the last two dimensions
print(arr[0, 0, :, :, :])      # accessing all elements in the last three dimensions
print(arr[0, :, :, :, :])       # accessing all elements in the last four dimensions
print(arr[:, :, :, :, :])        # accessing all elements in the 5-D array

# example of negative indexing in a 1-D array
print(a[-1])  # last element
print(a[-3:-1])  # elements from index -3 to -2
print(a[-4:])  # last four elements
print(a[:-2])  # all elements except the last two       

# example of negative indexing in a 2-D array
print(b[-1, :])  # last row
print(b[:, -1])  # last column
print(b[-2:, -2:])  # last two rows and last two columns
print(b[:-1, :-1])  # all rows and columns except the last one      
# example of negative indexing in a 3-D array
print(c[-1, :, :])  # last block
print(c[:, -1, :])  # all blocks, last row
print(c[:, :, -1])  # all blocks, all rows, last column
print(c[-1, -1, -1])  # last element in the last block

arr = np.array([[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]]) 
# From the second element, slice elements from index 1 to index 4 (not included): 
print(arr[1, 1:4])

arr = np.array([[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]]) 
# From both elements, return index 2: 
print(arr[0:2,2])

arr = np.array([[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]]) 
#From both elements, slice index 1 to index 4 (not included): 
print(arr[0:2,1:4])

