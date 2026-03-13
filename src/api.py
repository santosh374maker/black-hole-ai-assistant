from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import numpy as np
import faiss
import os
import requests
from sentence_transformers import SentenceTransformer

app = FastAPI()

# ======================
# Global variables
# ======================

embedding_model = None
index = None
documents = None

conversation_memory = []
MAX_MEMORY = 6

# ======================
# Request Model
# ======================

class Question(BaseModel):
    question: str

# ======================
# Startup Event
# ======================

@app.on_event("startup")
def load_resources():

    global embedding_model, index, documents

    print("Loading resources...")

    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

    df = pd.read_csv("data/chunks.csv")
    documents = df["chunk"].tolist()

    index_path = "data/vector_db.index"

    if not os.path.exists(index_path):

        print("Creating FAISS index...")

        embeddings = embedding_model.encode(documents)
        embeddings = np.array(embeddings).astype("float32")

        dimension = embeddings.shape[1]

        index = faiss.IndexFlatL2(dimension)
        index.add(embeddings)

        faiss.write_index(index, index_path)

    else:

        print("Loading FAISS index...")
        index = faiss.read_index(index_path)

    print("System ready.")

# ======================
# Health Check
# ======================

@app.get("/")
def health():
    return {"status": "Black Hole AI Assistant running"}

# ======================
# Retrieval
# ======================

def retrieve_documents(query):

    query_embedding = embedding_model.encode([query])
    query_embedding = np.array(query_embedding).astype("float32")

    D, I = index.search(query_embedding, 3)

    top_chunks = [documents[i] for i in I[0]]

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
# LLM Call (Groq)
# ======================

def call_llm(prompt):

    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

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

    response = requests.post(url, headers=headers, json=data)

    result = response.json()

    return result["choices"][0]["message"]["content"]

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