import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# load chunks
df = pd.read_csv("../data/chunks.csv")
chunks = df["chunk"].tolist()

# load FAISS index
index = faiss.read_index("../data/vector_db.index")

# load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

print("RAG retrieval system ready.")

while True:

    query = input("\nAsk a space question (type 'exit' to stop): ")

    if query.lower() == "exit":
        break

    # convert question to embedding
    query_embedding = model.encode([query])

    # search FAISS
    k = 3
    distances, indices = index.search(np.array(query_embedding), k)

    print("\nTop relevant chunks:\n")

    for i in indices[0]:
        print(chunks[i])
        print("\n----------------------------\n")