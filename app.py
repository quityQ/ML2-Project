import streamlit as st
import os
import tempfile
from database.data import Data
from streamlit_chat import message
from chatbot.chatbot import Chatbot

st.set_page_config(page_title="Chat")

data_instance = Data(player_id=None)
recentHeroes = []

def display_messages():
    st.subheader("Chat")
    for i, (msg, is_user) in enumerate(st.session_state["messages"]):
        message(msg, is_user=is_user, key=str(i))
    st.session_state["thinking_spinner"] = st.empty()
    st.session_state["user_input"] = ""

def process_input():
    memory = st.session_state["assistant"].get_history("1")
    if st.session_state["user_input"] and len(st.session_state["user_input"].strip()) > 0:
        user_text = st.session_state["user_input"].strip()
        with st.session_state["thinking_spinner"], st.spinner(f"Thinking"):
            agent_text = st.session_state["assistant"].ask(user_text)
            memory.add_message(user_text)
            memory.add_message(agent_text)

        st.session_state["messages"].append((user_text, True))
        st.session_state["messages"].append((agent_text, False))

def ingestGames():
    playerID = st.session_state["playerID"]
    st.session_state["ingestion_spinner"].text("Getting recent heroes...")

    with st.spinner("Getting recent heroes..."):
        recentHeroesList = data_instance.get_recent_heroes(playerID)
        recentHeroes = ", ".join(recentHeroesList)

    st.session_state["ingestion_spinner"].text("Recent heroes obtained!")

    st.session_state["ingestion_spinner"].empty()

    ingestGuides()

    with st.spinner("Checking recent games..."):
        init_agent_text = st.session_state["assistant"].ask("Here are some heroes I've been playing" + recentHeroes + "What should I do in order to improve?")
    st.session_state["ingestion_spinner"].empty()    
    st.session_state["messages"].append((init_agent_text, False))

def ingestGuides():
    st.session_state["ingestion_spinner"].text("Loading hero guides...")
    with st.spinner("Loading hero guides..."):
        guides = data_instance.get_hero_guides()
        st.session_state["assistant"].ingest(guides)
    pass
    st.session_state["ingestion_spinner"].empty()

def page():
    if len(st.session_state) == 0:
        st.session_state["messages"] = []
        st.session_state["assistant"] = Chatbot()

    st.header("Dota 2 Buddy")

    st.subheader("Enter you Player ID to get started:")
    st.text_input("Enter your player ID", key="playerID", max_chars=9)
    st.button("Get recent games", key="button", on_click=ingestGames)
    
    st.session_state["ingestion_spinner"] = st.empty()

    display_messages()
    st.text_input("Message", key="user_input", on_change=process_input)


if __name__ == "__main__":
    page()