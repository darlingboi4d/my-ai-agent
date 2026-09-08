import os
import json
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

from tools import TOOL_SCHEMAS, call_tool

load_dotenv()

# ----------------------------------------------------------------------
# Page setup — CHANGE THIS to match your project
# ----------------------------------------------------------------------
st.set_page_config(page_title="My AI Agent", page_icon="🤖")
st.title("🤖 Market Price Assistant")
st.caption("Ask me about food prices, totals, and comparisons.")

SYSTEM_PROMPT = """You are a helpful market price assistant for Nigerian shoppers.
Always use your tools to get real prices — never guess.
Give warm, practical answers and show your workings clearly."""

# ----------------------------------------------------------------------
# API key: works locally (.env) AND deployed (Streamlit secrets)
# ----------------------------------------------------------------------
def get_api_key():
    key = os.getenv("OPENAI_API_KEY")
    if key:
        return key
    try:
        return st.secrets["OPENAI_API_KEY"]
    except Exception:
        return None

api_key = get_api_key()
if not api_key:
    st.error("No API key found. Add OPENAI_API_KEY to your .env file (local) "
             "or to your Streamlit Cloud secrets (deployed).")
    st.stop()

client = OpenAI(api_key=api_key)
MODEL = "gpt-4o-mini"

# ----------------------------------------------------------------------
# Conversation memory
# ----------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# Replay the conversation so far
for msg in st.session_state.messages:
    role = msg["role"] if isinstance(msg, dict) else msg.role
    if role in ("user", "assistant"):
        content = msg["content"] if isinstance(msg, dict) else msg.content
        if content:
            with st.chat_message(role):
                st.markdown(content)

# ----------------------------------------------------------------------
# Chat input + the agent loop
# ----------------------------------------------------------------------
if prompt := st.chat_input("Ask me something..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        # --- The agent loop: keep going until no more tools are needed ---
        with st.status("Thinking...", expanded=True) as status:
            while True:
                response = client.chat.completions.create(
                    model=MODEL,
                    messages=st.session_state.messages,
                    tools=TOOL_SCHEMAS,
                )
                message = response.choices[0].message

                if not message.tool_calls:
                    break

                st.session_state.messages.append(message)

                for tool_call in message.tool_calls:
                    name = tool_call.function.name
                    args = json.loads(tool_call.function.arguments)
                    st.write(f"🔧 Using **{name}**")

                    try:
                        result = call_tool(name, args)
                    except Exception as e:
                        result = f"Tool error: {e}"

                    st.write(f"↳ {result}")
                    st.session_state.messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": str(result),
                    })

            status.update(label="Done!", state="complete", expanded=False)

        # --- Stream the final answer ---
        def stream_answer():
            stream = client.chat.completions.create(
                model=MODEL,
                messages=st.session_state.messages,
                stream=True,
            )
            for chunk in stream:
                piece = chunk.choices[0].delta.content or ""
                if piece:
                    yield piece

        answer = st.write_stream(stream_answer())
        st.session_state.messages.append({"role": "assistant", "content": answer})

# ----------------------------------------------------------------------
# Sidebar
# ----------------------------------------------------------------------
with st.sidebar:
    st.header("About")
    st.write("This agent uses tools to answer your questions.")
    if st.button("Clear conversation"):
        st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        st.rerun()