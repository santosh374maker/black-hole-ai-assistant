import streamlit as st
import requests
import uuid

API_URL = "http://localhost:8000/ask"

st.set_page_config(
    page_title="Black Hole",
    page_icon="⚫",
    layout="wide"
)

st.title("⚫ Black Hole")

# ---------------------------
# Session State Setup
# ---------------------------

if "chats" not in st.session_state:
    st.session_state.chats = {}

if "current_chat" not in st.session_state:
    chat_id = str(uuid.uuid4())
    st.session_state.current_chat = chat_id
    st.session_state.chats[chat_id] = []

# ---------------------------
# Sidebar
# ---------------------------

st.sidebar.title("Chat History")

if st.sidebar.button("New Chat"):

    chat_id = str(uuid.uuid4())

    st.session_state.current_chat = chat_id
    st.session_state.chats[chat_id] = []

# Show chat list
for chat_id in st.session_state.chats:

    if st.sidebar.button(f"Chat {list(st.session_state.chats.keys()).index(chat_id)+1}"):

        st.session_state.current_chat = chat_id

messages = st.session_state.chats[st.session_state.current_chat]

# ---------------------------
# Display Messages
# ---------------------------

for message in messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------------------
# Chat Input
# ---------------------------

prompt = st.chat_input("Ask a space question...")

if prompt:

    messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    response = requests.post(
        API_URL,
        json={"question": prompt}
    )

    result = response.json()

    answer = result["answer"]

    with st.chat_message("assistant"):
        st.markdown(answer)

    messages.append({"role": "assistant", "content": answer})