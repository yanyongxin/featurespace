'''
Created on May 4, 2023

@author: yanyo
'''
import pandas as pd

# create a DataFrame
data = {'name': ['Alice', 'Bob', 'Charlie', 'David'],
        'age': [25, 30, 35, 40]}
df = pd.DataFrame(data)

# sort the DataFrame by age in descending order
df = df.sort_values('age', ascending=False)

# reset the index labels
df = df.reset_index(drop=True)

# access a row using its index label
print(df.loc[0])
