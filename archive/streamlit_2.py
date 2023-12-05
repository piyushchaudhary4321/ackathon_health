import streamlit as st
import openai
from openai import OpenAI
import requests

# Define the base URL for ChatGPT API
API_BASE_URL = "https://api.openai.com/v1/chat/completions"

# Define your OpenAI API key
API_KEY = "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"

# Set the headers for API requests
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}


# Set your OpenAI API key
client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key="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",
)


# Initialize conversation history
conversation_history = []


# Streamlit app
st.title('GPT-3 Chatbot')

# Function to interact with GPT-3 and remember conversation
def interact_with_gpt(input_text):
    data = {
        'model':"gpt-3.5-turbo",
        'messages':[
            {"role": "system", "content": input_text},
            {"role": "user", "content": conversation_history[-1] if conversation_history else ""}
        ]
    }
    conversation_history.extend([input_text, response_data["choices"][0]["message"]["content"]])
    response = requests.post(API_BASE_URL, headers=headers, json=data)
    response_data = response.json()    
    
    return response_data["choices"][0]["message"]["content"]
    # reply = response['choices'][0].message.content
    # conversation_history.extend([input_text, reply])
    # return reply

# Streamlit interface
user_input = st.text_input("You:", "")
if st.button("Send"):
    if user_input:
        conversation_history.append(user_input)
        bot_reply = interact_with_gpt(user_input)
        st.text_area("Bot:", bot_reply)
