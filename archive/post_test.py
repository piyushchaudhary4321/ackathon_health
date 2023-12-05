import streamlit as st
import requests

def send_post_request(url, data):
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            return f"Error: {response.status_code} - {response.text}"
    except requests.RequestException as e:
        return f"Request Exception: {e}"

# Streamlit UI
st.title('Post Request Example')
url = st.text_input('Enter URL to send POST request:', 'https://example.com/api')
data = st.text_area('Enter JSON data:', '{"key": "value"}')
submit_button = st.button('Send POST Request')

if submit_button:
    result = send_post_request(url, data)
    st.write('Response:')
    st.json(result)