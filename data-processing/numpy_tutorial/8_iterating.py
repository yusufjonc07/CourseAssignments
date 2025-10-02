import numpy as np 

# Iterating Over Arrays

# Iterate through a 1-D array:
arr = np.array([1, 2, 3]) 
for x in arr: 
     print(x)

# Iterate through a 2-D array:
arr2d = np.array([[1, 2, 3], [4, 5, 6]])
for row in arr2d:
    for col in row:
        print(col)
        
# Iterate through a 3-D array:
arr = np.array([[1, 2, 3], [4, 5, 6]]) 
for x in arr: 
	for y in x: 
		print(y)

# Iterate through a 3-D array:
arr = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
for x in np.nditer(arr):
	print(x)


# Iterating With Different Step Size

print("\n\nIterate through every scalar element of the 2D array skipping 1 element:")

import numpy as np
arr = np.array([[1, 2, 3, 4], [5, 6, 7, 8]])
for x in np.nditer(arr[:, ::2]):
	print(x)
