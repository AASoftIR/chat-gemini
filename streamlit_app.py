# import streamlit as st
# import pandas as pd

# st.title("Pandas Dataframe")

# df = pd.DataFrame({
#     'first column': [1, 2, 3, 4],
#     'second column': [10, 20, 30, 40],
# })

# st.data_editor(df)

# st.header("Metrics")

# mean = df['first column'].mean()
# median = df['first column'].median()
# std = df['first column'].std()
# min = df['first column'].min()
# max = df['first column'].max()

# st.write(f"Mean: {mean}")
# st.write(f"Median: {median}")
# st.write(f"Standard Deviation: {std}")
# st.write(f"Minimum: {min}")
# st.write(f"Maximum: {max}")


# with st.form("my_form",clear_on_submit=True):
#     name = st.text_input('Name')
#     submitted = st.form_submit_button("Submit")
#     if submitted:
#         st.write(f"Hello {name}!")
#         st.balloons()


# if "c" not in st.session_state:
#     st.session_state.c = 0
    
# if st.button("Increment"):
#     st.session_state.c += 1
# st.write(f"Count: {st.session_state.c}")
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