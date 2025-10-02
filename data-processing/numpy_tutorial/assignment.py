import numpy as np

# 1.	Import numpy as np and see the version.
print(np.__version__) # Resulted: 2.2.6

# # 2.	Create a 1D array of numbers from 2 to 11
# arr = np.arange(2, 12)
# print(arr)

def check_odd(num):
    return num % 2 != 0



# 3.	Extract all odd numbers from arr
arr = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10, 11,12])
odd_numbers = arr[check_odd(arr)]
print(odd_numbers)

# arr = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10])
# # 4.	Replace all odd numbers in arr with -1
# arr[arr % 2 != 0] = -1
# print(arr)

# # 5.	Create a 3×3 numpy array of all True’s
# true_array = np.full((3, 3), True)
# print(true_array)
