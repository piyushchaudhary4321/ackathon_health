
import streamlit as st
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

# Function to generate a response using ChatGPT API
def generate_gpt_response(base_file):
    data = {
        "model": "gpt-3.5-turbo",
        "messages": base_file
    }
    response = requests.post(API_BASE_URL, headers=headers, json=data)
    response_data = response.json()
    # conversation_history.extend(response_data["choices"][0]["message"]["content"])
    return response_data["choices"][0]["message"]["content"]

# Streamlit app
def streamlit_app():
    st.title("Acko Care")
    st.subheader("Welcome to your personal Life Insurance Helper! Answer the following questions to secure yourself")

    # User input
    user_input = st.text_input("")

    if user_input:
        requests.post('http://localhost:8502/',{'data':user_input})
        if 'conversation_history' not in st.session_state:
            st.session_state['conversation_history'] = []
        if st.session_state['conversation_history'] == []:
            base_data = [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": user_input}]
            data = {
                "model": "gpt-3.5-turbo",
                "messages": base_data
            }
        else:
            for number, message in enumerate(st.session_state['conversation_history']):
                base_data = []
                if number % 2 == 1:
                    role_model = 'assistant'
                    new_data = [{'role': role_model, 'content':st.session_state['conversation_history'][number]}]
                    base_data += new_data
                else:
                    role_model = 'user'
                    new_data = [{'role': role_model, 'content':st.session_state['conversation_history'][number]}]
                    base_data += new_data

        st.session_state['conversation_history'].extend([user_input])

        # conversation_history.extend([user_input, generate_gpt_response(user_input)])
        # Generate response
        response = generate_gpt_response(base_data)
        st.session_state['conversation_history'].extend([response])
        # Display response
        st.text_area('test', value=response, height=200)

# Run the app
if __name__ == "__main__":
    streamlit_app()


