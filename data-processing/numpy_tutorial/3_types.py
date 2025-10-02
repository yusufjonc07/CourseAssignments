# data types in numpy
import numpy as np

# example of different data types
int_array = np.array([1, 2, 3], dtype=np.int32)
float_array = np.array([1.2344, 2.344, 3.876], dtype=np.float64)
complex_array = np.array([1+2j, 3+4j], dtype=np.complex128)
bool_array = np.array([True, False, True], dtype=np.bool_)
str_array = np.array(['apple', 'banana', 'cherry'], dtype=np.str_)
object_array = np.array([1, 'two', 3.0], dtype=np.object_)

# print("Integer Array:", int_array, int_array.dtype)
# print("Float Array:", float_array, float_array.dtype)
# print("Complex Array:", complex_array, complex_array.dtype)
# print("Boolean Array:", bool_array, bool_array.dtype)
print("String Array:", str_array, str_array.dtype)
# print("Object Array:", object_array, object_array.dtype)    