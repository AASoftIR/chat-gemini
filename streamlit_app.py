import streamlit as st
import requests
import json

# Title
st.title("💬 Chatbot of Gemini")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

# Display existing chat messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Function to handle streaming API call with context
def stream_response():
    api_key = st.secrets["openai_api_key"]
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:streamGenerateContent?alt=sse&key={api_key}"
    headers = {"Content-Type": "application/json"}

    # Prepare messages for API request, maintaining context from all previous messages
    conversation = [{"role": msg["role"], "parts": [{"text": msg["content"]}]} for msg in st.session_state["messages"]]
    data = {"contents": conversation}

    # Start SSE request
    with requests.post(url, headers=headers, json=data, stream=True) as response:
        response.raise_for_status()
        
        # Temporary buffer to collect streamed response
        message = ""

        # Stream through the response chunks
        for line in response.iter_lines():
            if line:
                try:
                    line_data = line.decode("utf-8").lstrip("data: ")
                    json_data = json.loads(line_data)

                    # Extract and append each part to the message buffer
                    parts = json_data.get("candidates", [{}])[0].get("content", {}).get("parts", [])
                    for part in parts:
                        message += part.get("text", "")
                except json.JSONDecodeError:
                    continue  # Skip non-JSON lines

        return message

# Accept user input and process it
if prompt := st.chat_input():
    if not st.secrets["openai_api_key"]:
        st.info("Please add your Gemini API key to continue.")
        st.stop()

    # Add user message to session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Get the full streaming response
    response_message = stream_response()

    # Append assistant message to session state after full response is completed
    st.session_state.messages.append({"role": "assistant", "content": response_message})
    st.chat_message("assistant").write(response_message)
