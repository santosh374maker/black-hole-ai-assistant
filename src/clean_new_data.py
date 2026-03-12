import pandas as pd
import re


def clean_text(text):

    text = re.sub(r"\[[0-9]*\]", "", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def clean_articles():

    df = pd.read_csv("data/new_data.csv")

    df["content"] = df["content"].apply(clean_text)

    df.to_csv("data/cleaned_new_data.csv", index=False)

    print("New data cleaned")