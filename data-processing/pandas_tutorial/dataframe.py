import pandas as pd
import numpy as np

df = pd.read_csv("pandas_tutorial/data/patient.csv", quotechar='"', sep=';')

ser = pd.Series(df['name'])
print(ser.head(10))

# print(df.info())
# print(df.describe())
# print(df.tail(10))
# print(df['age'].mean())
# print(df['age'].max())
# print(df['age'].min())
print(df.ta)