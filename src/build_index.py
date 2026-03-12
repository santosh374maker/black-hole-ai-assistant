import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

print("Loading data...")

df = pd.read_csv("data/chunks.csv")

chunks = df["chunk"].tolist()

print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Creating embeddings...")

embeddings = model.encode(chunks)

embeddings = np.array(embeddings).astype("float32")

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embeddings)

print("Saving index...")

faiss.write_index(index, "data/vector_db.index")

print("VECTOR DB index built successfully.")