import pandas as pd
import numpy as np
import faiss
import requests
from sentence_transformers import SentenceTransformer

# load chunk data
df = pd.read_csv("../data/chunks.csv")
chunks = df["chunk"].tolist()

# load FAISS index
index = faiss.read_index("../data/vector_db.index")

# load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

print("Space AI Assistant Ready 🚀")

while True:

    question = input("\nAsk a space question (type 'exit' to quit): ")

    if question.lower() == "exit":
        break

    # create query embedding
    query_embedding = model.encode([question])

    # search FAISS
    k = 3
    distances, indices = index.search(np.array(query_embedding), k)

    context = ""

    for i in indices[0]:
        context += chunks[i] + "\n"

    # build prompt
    prompt = f"""
You are a space research assistant.

Use the context below to answer the question.

Context:
{context}

Question:
{question}

Answer:
"""

    # send prompt to Ollama (Mistral)
    response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "mistral:7b-instruct-q4_0",
        "prompt": prompt,
        "stream": False
    }
)

    data = response.json()

    if "response" in data:
        answer = data["response"]
    else:
        print("Error from Ollama:", data)
        continue


    answer = response.json()["response"]

    print("\nAI Answer:\n")
    print(answer)