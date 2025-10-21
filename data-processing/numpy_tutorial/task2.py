import numpy as np

data = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [1, 2, 3],  # duplicate 1
    [7, 8, 9],
    [4, 5, 6]   # duplicate 2
])

print("Original Data:")
print(data)

unique_data, unique_indices = np.unique(data, axis=0, return_index=True)
unique_data = unique_data[np.argsort(unique_indices)]  # we keep original order

print("\nData after removing duplicates:")
print(unique_data)

indices = np.arange(len(unique_data))
print("\nReset index:")
print(indices)

ids = unique_data[:, 0]  # first column is ID
is_unique = len(ids) == len(np.unique(ids))
print("\nAre IDs unique?:", is_unique)

_, unique_indices_all, counts = np.unique(data, axis=0, return_index=True, return_counts=True)
duplicates = data[unique_indices_all[counts > 1]]

print("\nDuplicate rows found:")
print(duplicates)
