# %load_ext autoreload
# %autoreload 2
from azure_response import response_generator
import streamlit as st
from conversation_conclusion import conclusion_processing


# Initialize conversation history
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

# Initialize conversation history for the iterator - This is the order in which it needs to be displayed
if 'conversation_history_iterator' not in st.session_state:
    st.session_state.conversation_history_iterator = []


# Display title and chat history
st.title("AckoCares")
st.subheader("Your Efficient Insurance Advisor from Acko!")

# Define function to display messages
def display_message(role, message):
    if role == 'user':
        st.write(f"🧔‍♂️: {message}")
    elif role == 'assistant':
        st.write(f"🤖: {message}")

def message_generator(conv_history):
    messages = [{"role":"system","content":"You are AckoCares, an adept insurance advisor at Acko Life Insurance. Your approach involves guiding customers efficiently through the policy purchasing process with ease and clarity. To facilitate this, ask one question at a time on key topics like KYC information, financial needs, physical risk factors, medical history, and lab selection for tests. After each question, offer 2-4 examples of possible responses or points to clarify details, but do this selectively to avoid overwhelming the customer. This method aims to simplify the customer's decision-making process, making it easier for them to respond without overthinking. Continue to emphasize flexibility in the process, allowing customers to pause and resume as needed, and accept document submissions via email or photos. Your interactions should be straightforward and reassuring, focusing on customer convenience and understanding."}]
    
    
    
    for role, message in conv_history:
        if role == 'user':
            messages.append({"role": "user", "content": message})
        elif role == 'assistant':
            messages.append({"role": "assistant", "content": message})
    return messages
    
    
# User input and sending messages
user_input = st.text_input("Type a message...", key="user_input1")
if user_input:
    st.session_state.conversation_history.append(('user', user_input))
    # Prepare the conversation history to be sent to OpenAI
    messages = message_generator(st.session_state.conversation_history)

    st.session_state.restored_messages = messages
    # Get Response
    response = response_generator(messages)

    # Extract AI's response from the completion
    reply = response['choices'][0]['message']['content']
    
    # Conversation History Append for the model
    st.session_state.conversation_history.append(('assistant', reply))

    # Conversation History append for the output
    st.session_state.conversation_history_iterator.append(('assistant', reply))
    st.session_state.conversation_history_iterator.append(('user', user_input))

    # Display existing conversation history including the AI's response above the text input box
    for role, message in st.session_state.conversation_history_iterator[::-1]:
        display_message(role, message)
    
    # Check for Conversation Conclusion and take Necessary Actions
    messages = message_generator(st.session_state.conversation_history)
    
    conclusion_detection = conclusion_processing(messages)
    # st.write(conclusion_detection.conclusion_detector())
    if conclusion_detection.conclusion_detector() == 'Yes':
        st.write('Thanks for reaching out! I hope I\'ve been able to help you address your life insurance needs')
        conclusion_detection.json_extractor()
    else:
        pass
    
    
