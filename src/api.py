from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import numpy as np
import faiss
import os
import requests
from sentence_transformers import SentenceTransformer, CrossEncoder

app = FastAPI()

print("Loading resources...")

# ======================
# Models
# ======================

embedding_model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")
reranker_model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

# ======================
# Load documents
# ======================

df = pd.read_csv("data/chunks.csv")
documents = df["chunk"].tolist()

# ======================
# VECTOR_DB Index
# ======================

index_path = "data/vector_db.index"

if not os.path.exists(index_path):

    print("Vector_db index not found. Creating index...")

    embeddings = embedding_model.encode(documents)
    embeddings = np.array(embeddings).astype("float32")

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    faiss.write_index(index, index_path)

    print("VECTOR_DB index created.")

else:

    print("Loading VECTOR_DB index...")
    index = faiss.read_index(index_path)

print("System ready.")

# ======================
# Conversation Memory
# ======================

conversation_memory = []
MAX_MEMORY = 6

# ======================
# Request Model
# ======================

class Question(BaseModel):
    question: str

# ======================
# Retrieval
# ======================

def retrieve_documents(query):

    query_embedding = embedding_model.encode([query])
    query_embedding = np.array(query_embedding).astype("float32")

    D, I = index.search(query_embedding, 5)

    candidates = [documents[i] for i in I[0]]

    pairs = [[query, doc] for doc in candidates]

    scores = reranker_model.predict(pairs)

    ranked = sorted(zip(candidates, scores),
                    key=lambda x: x[1],
                    reverse=True)

    top_chunks = [chunk for chunk, score in ranked[:2]]

    context = "\n\n".join(top_chunks)

    return context, top_chunks

# ======================
# Prompt Builder
# ======================

def build_prompt(question, context):

    history = "\n".join(conversation_memory)

    prompt = f"""
You are a helpful space science AI assistant.

Conversation History:
{history}

Relevant Knowledge:
{context}

User Question:
{question}

Answer clearly and scientifically.
"""

    return prompt

# ======================
# LLM Call
# ======================

def call_llm(prompt):

    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    if GROQ_API_KEY:

        url = "https://api.groq.com/openai/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "llama3-8b-8192",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        try:

            response = requests.post(url, headers=headers, json=data)
            result = response.json()

            return result["choices"][0]["message"]["content"]

        except Exception as e:

            print("Groq error:", e)

    # fallback to ollama

    try:

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral:7b-instruct-q4_0",
                "prompt": prompt,
                "stream": False
            }
        )

        return response.json()["response"]

    except:

        return "LLM is not available."

# ======================
# Ask Endpoint
# ======================

@app.post("/ask")
def ask_question(q: Question):

    question = q.question

    context, sources = retrieve_documents(question)

    prompt = build_prompt(question, context)

    answer = call_llm(prompt)

    conversation_memory.append(f"User: {question}")
    conversation_memory.append(f"Assistant: {answer}")

    if len(conversation_memory) > MAX_MEMORY:

        conversation_memory.pop(0)
        conversation_memory.pop(0)

    return {
        "answer": answer,
        "sources": sources
    }

# ======================
# Reset Chat
# ======================

@app.post("/reset")
def reset_chat():

    global conversation_memory

    conversation_memory = []

    return {"message": "Conversation reset"}