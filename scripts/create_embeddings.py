import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

df = pd.read_csv("data/chunks.csv")

chunks = df["chunk"].tolist()

model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = model.encode(chunks)

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(np.array(embeddings))

faiss.write_index(index, "data/vector_db.index")

print("Vector_db index created:", index.ntotal)