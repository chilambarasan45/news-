"""
══════════════════════════════════════════════
STREAMLIT UI for Smart News Assistant
══════════════════════════════════════════════
Imports the existing handle_user_message() function — no chatbot
logic duplicated here.

Run with:
    streamlit run ui.py
══════════════════════════════════════════════
"""

import asyncio
import streamlit as st

from supervisor import handle_user_message

st.set_page_config(
    page_title="Smart News Assistant",
    page_icon="🤖",
    layout="centered",
)

st.title("🤖 Smart News Assistant")
st.caption("Ask me about News, Stocks, Weather, or get a Summary of any topic.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


def run_async(coro):
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)


user_input = st.chat_input("Type your question... e.g. 'give me cricket news'")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response_text = run_async(handle_user_message(user_input))
        st.markdown(response_text)

    st.session_state.messages.append({"role": "assistant", "content": response_text})

with st.sidebar:
    st.header("💡 Try asking")
    st.markdown(
        "- 📰 Give me cricket news\n"
        "- 📈 What is Tesla stock price?\n"
        "- 🌤️ Weather in Chennai\n"
    )
    st.divider()
    if st.button("🗑️ Clear chat"):
        st.session_state.messages = []
        st.rerun()
