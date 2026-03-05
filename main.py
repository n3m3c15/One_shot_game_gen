import streamlit as st
import streamlit.components.v1 as components
import os
from Agents.game_description_agent import EnquiryAgent

REGISTRY_FILE = "current_game.txt"

# Helper: Read Current Game
# Post generation game_generation_agent adds the entry point path into current_game.txt
# TODO: improve game rendering condition...ideally by using a backend you lazy bum
def get_current_game_dir():
    if os.path.exists(REGISTRY_FILE):
        with open(REGISTRY_FILE, "r") as f:
            return f.read().strip()
    return None


# Initialize Session 

if "agent" not in st.session_state:
    st.session_state.agent = EnquiryAgent()

if "messages" not in st.session_state:
    st.session_state.messages = [
        m for m in st.session_state.agent.messages if m["role"] != "system"
    ] ### avoid displaying system_prompt + skill.md in history

agent = st.session_state.agent
messages = st.session_state.messages

st.title("🎮 Game Description Agent")

# Display Chat History


for msg in messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Handle User Input

user_input = st.chat_input("Type your message...")

if user_input:

    # Quiting Logic

    if user_input.lower() in ["/quit", "/q"]:

        st.session_state.agent = EnquiryAgent()
        st.session_state.messages = [
            m for m in st.session_state.agent.messages if m["role"] != "system"
        ]

        if os.path.exists(REGISTRY_FILE):
            os.remove(REGISTRY_FILE)

        st.success("Session reset.")
        st.rerun()

    # Show user message
    with st.chat_message("user"):
        st.markdown(user_input)

    messages.append({"role": "user", "content": user_input})

    # Call Agent
    with st.chat_message("assistant"):
        with st.spinner("Agent thinking..."):
            response = agent(user_prompt=user_input)
            st.markdown(response)

    messages.append({"role": "assistant", "content": response})

    st.rerun()

# Render Generated Game in iframe
#TODO: This seems to be buggy af make a backend and fix it for the love of all thats holy
st.divider()
st.header("🕹️ Play Generated Game")

game_dir = get_current_game_dir()

if game_dir:

    game_path = game_dir

    if os.path.exists(game_path):

        st.success(f"Game ready: {game_dir}")

        with open(game_path, "r", encoding="utf-8") as f:
            game_html = f.read()

        components.html(game_html, height=750, scrolling=False)

        # Download button
        # TODO: IDEK if this works I forgot to test it post dockerizing now it's 2am and I can't bother no more
        # get into software they said, it'll be fun they said T_T
        with open(game_path, "r", encoding="utf-8") as f:
            st.download_button(
                label="📥 Download Game",
                data=f.read(),
                file_name="index.html",
                mime="text/html"
            )

    else:
        st.info("Game is being generated...")

else:
    st.info("No game generated yet.")
