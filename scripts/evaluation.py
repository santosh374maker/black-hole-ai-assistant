import pandas as pd

df = pd.read_csv("/data/chunks.csv")

print("Total chunks:", len(df))

avg_length = df["chunk"].apply(len).mean()

print("Average chunk length:", avg_length)