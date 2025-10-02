# Flattening the arrays 

# Means converting a multidimensional array into a 1D array. 

# Use reshape(-1) to do this. 

# Example: 
import numpy as np 
arr = np.array([[1, 2, 3], [4, 5, 6]]) 
print(arr) 
newarr = arr.reshape(-1)     
# Convert the array into a 1D array: 
print("Flattened array:", newarr)
