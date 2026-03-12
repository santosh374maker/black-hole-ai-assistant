import pandas as pd
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


def update_index():

    print("Updating vector database...")

    model = SentenceTransformer("all-MiniLM-L6-v2")

    old_df = pd.read_csv("data/chunks.csv")

    new_df = pd.read_csv("data/new_chunks.csv")

    combined = pd.concat([old_df, new_df], ignore_index=True)

    combined.to_csv("data/chunks.csv", index=False)

    chunks = combined["chunk"].tolist()

    embeddings = model.encode(chunks)

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(np.array(embeddings))

    faiss.write_index(index, "data/vector_db.index")

    print("Vector database updated successfully")