import pandas as pd
import re

# load raw dataset
df = pd.read_excel("../data/Raw_data.xlsx")

print("Original rows:", len(df))

def clean_text(text):

    text = str(text)

    # remove citations like [1], [2]
    text = re.sub(r"\[\d+\]", "", text)

    # remove newline characters
    text = text.replace("\n", " ").replace("\t", " ")

    # remove strange symbols
    text = re.sub(r"[^a-zA-Z0-9.,!? ]", "", text)

    # remove multiple spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()

# apply cleaning
df["content"] = df["content"].apply(clean_text)

# remove empty rows
df = df[df["content"].str.len() > 50]

print("Cleaned rows:", len(df))

# save cleaned dataset
df.to_csv("../data/cleaned_data.csv", index=False)

print("Clean dataset saved.")