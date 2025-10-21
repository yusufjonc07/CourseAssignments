# import pandas and numpy
import pandas as pd 
import numpy as np

# creating simple array
data = np.array(['e', 'r', 'e', 'g', 'k', 'e', 's', 'f'])

# creating series from array
ser = pd.Series(data)

# retrieve the first element
print('\n\nFirst element:', ser[0])
print('\n\nFirst five elements:', ser[:5])
print('\n\nLast six elements:', ser[-6:])