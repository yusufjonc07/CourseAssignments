
# Convert the following 1-D array with 12 elements into a 2-D array. 
import numpy as np 
arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]) 
newarr = arr.reshape(
    6 , # number of rows
    2   # number of columns   
) 
#The outermost dimension will have 4 arrays, each with 3 elements: 
print(newarr)



#Convert the following 1-D array with 12 elements into a 3-D array. 

arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]) 
newarr = arr.reshape(2, 3, 2) 
#The outermost dimension will have 2 arrays that contain 3 arrays, each with 2 elements: 
print(newarr)

# Convert 1D array with 8 elements to 3D array with 2x2 elements

arr = np.array([1, 2, 3, 4, 5, 6, 7, 8]) 
newarr = arr.reshape(2, 2, 2) 

"""The outermost dimension will have 2 arrays that contain 2 arrays, each with 2 elements: """
print(newarr)
