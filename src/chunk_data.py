import pandas as pd

df = pd.read_csv("data/clean_articles.csv")

chunks = []

chunk_size = 400
overlap = 50

for _, row in df.iterrows():

    text = row["content"]
    title = row["title"]

    start = 0

    while start < len(text):

        chunk = text[start:start+chunk_size]

        chunks.append({
            "title": title,
            "chunk": chunk
        })

        start += chunk_size - overlap

chunks_df = pd.DataFrame(chunks)

chunks_df.to_csv("data/chunks.csv", index=False)

print("Chunks created:", len(chunks_df))