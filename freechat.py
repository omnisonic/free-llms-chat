import streamlit as st
from openai import OpenAI
from os import getenv
import requests

# Define the LLM engines and their corresponding IDs
llm_engines = {
    "llama-3-8b-instruct": "meta-llama/llama-3-8b-instruct:free",
    "zephyr-7b-beta": "huggingfaceh4/zephyr-7b-beta:free",
    "cinematika-7b": "openrouter/cinematika-7b:free",
    "mistralai/mistral-7b-instruct:free": "mistralai/mistral-7b-instruct:free",
    "gemma-7b-it": "google/gemma-7b-it:free",
    "nous-capybar":"nousresearch/nous-capybara-7b:free",
    "openchat": "openchat/openchat-7b:free",
    "topy-m-7b": "undi95/toppy-m-7b:free",

}

# Initialize the selected LLM engine
selected_llm_engine = "meta-llama/llama-3-8b-instruct:free"

# Create the Streamlit app
st.title("LLM Chat App")
with st.sidebar:
    # Create the toggle buttons for selecting the LLM engine
    llm_engines_list = list(llm_engines.values())
    selected_llm_engine = st.radio(
        "Select the LLM engine:",
        llm_engines_list
    )

st.write("You selected:", selected_llm_engine)


if "messages" not in st.session_state:
    st.session_state["messages"] = []  # Initialize an empty list for chat messages
    print(" Line ~250 session state messages initialized")
# # Update the selected LLM engine
# selected_engine_id = llm_engines[selected_llm_engine]
prompt = st.chat_input("Ask a question...", key="chat_input")


for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])




if prompt:

    # gets API Key from environment variable OPENAI_API_KEY
    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=getenv("OPENROUTER_API_KEY"),
    )
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(
    #   extra_headers={
    #     "HTTP-Referer": $YOUR_SITE_URL, # Optional, for including your app on openrouter.ai rankings.
    #     "X-Title": $YOUR_APP_NAME, # Optional. Shows in rankings on openrouter.ai.
    #   },
    model=selected_llm_engine,
    messages=[
        {
        "role": "system",
        "content": "You are a helpful chatbot",
        },
    ]+ st.session_state.messages + [{"role": "user", "content": prompt}],
        )
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)



