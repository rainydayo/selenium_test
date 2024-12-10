import pandas as pd

df = pd.read_csv('Processed_2017.csv')

df = df.iloc[1500:]

df.to_csv("2017_1.5_2k.csv", index=False)