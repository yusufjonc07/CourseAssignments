# Joining NumPy Arrays

# Example: Join two arrays

import numpy as np

print("Join two arrays:")
arr1 = np.array([1, 2, 3])
arr2 = np.array([4, 5, 6])
arr = np.concatenate((arr1, arr2))
print("Joined array:", arr)

print("\nJoin two 2-D arrays:")
arr1 = np.array([[1, 2], [3, 4]])
arr2 = np.array([[5, 6], [7, 8]])
arr = np.concatenate((arr1, arr2))
print(arr)

print("\n\nJoin two 3-D arrays along axis 0:")
arr1 = np.array([[[1, 2], [3, 4]],[[1, 2], [3, 4]]])
arr2 = np.array([[[5, 6], [7, 8]],[[5, 6], [7, 8]]])
arr = np.concatenate((arr1, arr2),axis=0)
print(arr)

print("\n\nJoin two 3-D arrays:")

import numpy as np
arr1 = np.array([[[1, 2], [3, 4]],[[1, 2], [3, 4]]])
arr2 = np.array([[[5, 6], [7, 8]],[[5, 6], [7, 8]]])
arr = np.concatenate((arr1, arr2),axis=2)
print(arr)


print("\n\nStacking arrays:")

arr1 = np.array([1, 2, 3])
arr2 = np.array([4, 5, 6])
arr = np.stack((arr1, arr2), axis=1)
print(arr)

print("\n\nHorizontal stacking:")
arr1 = np.array([1, 2, 3])
arr2 = np.array([4, 5, 6])
arr = np.hstack((arr1, arr2))
print(arr)




