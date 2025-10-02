# Conversion between different data types
import numpy as np

# Convert a list to a numpy array
list_data = [1, 2, 3, 4, 5]
array_from_list = np.array(list_data)
print("Array from list:", array_from_list)
print("Data type:", array_from_list.dtype)
# Convert a tuple to a numpy array
tuple_data = (1, 2, 3, 4, 5)
array_from_tuple = np.array(tuple_data)
print("Array from tuple:", array_from_tuple)
print("Data type:", array_from_tuple.dtype)
# Convert a numpy array to a list
array_to_list = array_from_list.tolist()
print("List from array:", array_to_list)
print("Type:", type(array_to_list))
# Convert a numpy array to a tuple
array_to_tuple = tuple(array_from_list)
print("Tuple from array:", array_to_tuple)
print("Type:", type(array_to_tuple))
# Convert a numpy array to a different data type
float_array = array_from_list.astype(np.float64)
print("Array with float data type:", float_array)
print("Data type:", float_array.dtype)
# Convert a numpy array to a pandas Series
import pandas as pd
series_from_array = pd.Series(array_from_list)
print("Pandas Series from array:\n", series_from_array)
print("Data type:", series_from_array.dtype)
# Convert a pandas Series to a numpy array
array_from_series = series_from_array.to_numpy()
print("Array from pandas Series:", array_from_series)
print("Data type:", array_from_series.dtype)
# Convert a numpy array to a pandas DataFrame
df_from_array = pd.DataFrame(array_from_list, columns=['Numbers'])
print("Pandas DataFrame from array:\n", df_from_array)
print("Data types:\n", df_from_array.dtypes)
# Convert a pandas DataFrame to a numpy array
array_from_df = df_from_array.to_numpy()
print("Array from pandas DataFrame:\n", array_from_df)
print("Data type:", array_from_df.dtype)        