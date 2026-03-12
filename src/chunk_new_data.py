import pandas as pd


def chunk_text(text, size=400):

    words = text.split()

    chunks = []

    for i in range(0, len(words), size):

        chunks.append(" ".join(words[i:i+size]))

    return chunks


def create_chunks():

    df = pd.read_csv("data/cleaned_new_data.csv")

    rows = []

    for _, row in df.iterrows():

        chunks = chunk_text(row["content"])

        for chunk in chunks:

            rows.append({
                "title": row["title"],
                "chunk": chunk
            })

    new_df = pd.DataFrame(rows)

    new_df.to_csv("data/new_chunks.csv", index=False)

    print("Chunks created")