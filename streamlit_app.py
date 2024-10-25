
import streamlit as st
import google.generativeai as genai
import os


st.title("💬 Chatbot of Gemini")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not st.secrets["openai_api_key"]:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    genai.configure(api_key=st.secrets["openai_api_key"])
    model = genai.GenerativeModel('gemini-1.5-flash')
    res = model.generate_content("The opposite of hot is")

    client = model
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = model.generate_content(st.session_state.messages[-1]["content"])
    msg = response.text

    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)