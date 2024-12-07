import pandas as pd

df = pd.read_csv('Processed_2018.csv')

df = df.iloc[:2792]

df.to_csv("new_2018.csv", index=False)