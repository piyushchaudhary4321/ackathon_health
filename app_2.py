# %load_ext autoreload
# %autoreload 2
from azure_response import response_generator
import streamlit as st
from conversation_conclusion import conclusion_processing
from system_message_appender import stage_controller
import re

# st.write(st.session_state.stage_tracker)
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
    messages = [{"role":"system",
                 "content":st.session_state.initial_prompt}]
    for role, message in conv_history:
        if role == 'user':
            messages.append({"role": "user", "content": message})
        elif role == 'assistant':
            messages.append({"role": "assistant", "content": message})
        elif role == 'system':
            messages.append({"role": "system", "content": message})
    return messages
    




# Initialize conversation history
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

# Initialize conversation history for the iterator - This is the order in which it needs to be displayed
if 'conversation_history_iterator' not in st.session_state:
    st.session_state.conversation_history_iterator = []

# Instantiate the class to provide initial prompt
initial_prompt_inst = stage_controller(st.session_state.conversation_history, '','')
st.session_state.initial_prompt = initial_prompt_inst.base_pitch

# Initialize Stage Tracker
if 'stage_tracker' not in st.session_state:
    st.session_state.stage_tracker = 1
    st.session_state.current_stage = 0
else:
    # st.write(response_generator("What is the current stage that the user is at. Give me a single number and no other text")['choices'][0]['message']['content'])
    # st.session_state.current_stage = int(response_generator("What is the current stage that the user is at. Give me a single number and no other text")['choices'][0]['message']['content'])
    try:
        temp_message = 'What is the current stage that the user is at. Give me a single number and no other text'
        messages = message_generator(st.session_state.conversation_history)
        messages.append({"role": "user", "content": temp_message})
        st.session_state.current_stage = int(response_generator(messages)['choices'][0]['message']['content'])
        st.write(st.session_state.current_stage)
    except:
        st.session_state.current_stage = 0






if (st.session_state.stage_tracker == 1) & (int(st.session_state.current_stage) <= 5):
    stage_initiation = stage_controller(st.session_state.conversation_history, '',5)
    st.session_state.stage_data = stage_initiation.json_reader(int(st.session_state.current_stage))


# User input and sending messages

user_input = st.text_input("Type a message...", key="user_input1")

if user_input:    
    messages = message_generator(st.session_state.conversation_history)
    if st.session_state.stage_tracker == 1:
        stage_initiation_internal = stage_controller(st.session_state.conversation_history, messages,st.session_state.stage_data)
        if st.session_state.current_stage == 0:
            initiation_instructions = stage_initiation_internal.stage0_instructions
        elif st.session_state.current_stage == 1:
            initiation_instructions = stage_initiation_internal.stage1_instructions
        elif st.session_state.current_stage == 2:
            initiation_instructions = stage_initiation_internal.stage2_instructions
        elif st.session_state.current_stage == 3:
            initiation_instructions = stage_initiation_internal.stage3_instructions
        elif st.session_state.current_stage == 4:
            initiation_instructions = stage_initiation_internal.stage4_instructions
        elif st.session_state.current_stage == 5:
            initiation_instructions = stage_initiation_internal.stage5_instructions
        elif st.session_state.current_stage == 6:
            initiation_instructions = stage_initiation_internal.stage6_instructions
        elif st.session_state.current_stage == 7:
            initiation_instructions = stage_initiation_internal.stage7_instructions
        st.session_state.conversation_history.append(('system', f'Judge the current State of the QnA and accordingly take the instructions for the questions to be asked from {initiation_instructions}. The Questions to be asked are present in {st.session_state.stage_data}. If No Questions are present just ask the relevant stage questions. Please keep track of the current State and don\'t change the State util all relevant questions are answered from the JSON file provided'))
        # messages = message_generator(st.session_state.conversation_history)
        # st.write(messages)
        st.session_state.stage_tracker = 0
    
    st.session_state.conversation_history.append(('user', user_input))

    # Prepare the conversation history to be sent to OpenAI
    messages = message_generator(st.session_state.conversation_history)
    
    
    # Append custom System message that depends on user input
    # st.session_state.conversation_history = system_message_input(st.session_state.conversation_history, messages)

    # Prepare message history again to account for system prepared using system_message_input
    # messages = message_generator(st.session_state.conversation_history)

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
    
    # Track Stage that the user is in
    stage_tracker_inst = stage_controller(st.session_state.conversation_history, messages,st.session_state.stage_data)
    stage_tracker_var = stage_tracker_inst.stage_complete_detector()

    # Extracting stage and Conversation end info and taking necessary actions
    try:
        stage = int(re.split(r'(:|,)',stage_tracker_var)[2].strip())
    except:
        stage = 0
    if 'yes' in str.lower(stage_tracker_var):
        # st.write('Thanks for reaching out! I hope I\'ve been able to help you address your life insurance needs')
        conclusion_detection = conclusion_processing(messages)
        conclusion_detection.json_extractor()
        conv_end = 'Yes'
        st.session_state.stage_tracker = stage
        st.write(stage)
    else:
        st.session_state.stage_tracker = stage
        st.write(stage)
        st.write(st.session_state.current_stage)
        # conv_end = 'No'
    

    # st.write(f"Stage Number is {str(stage)}. Conversation End is {conv_end}")    
    # st.write(f"The message is {stage_tracker_var[10]}")
    # st.write(stage_tracker_var[10])
    # if 'no' in str.lower(stage_tracker_var):
    #     st.write('No')

    # conclusion_detection = conclusion_processing(messages)
    # # st.write(conclusion_detection.conclusion_detector())
    # if conclusion_detection.conclusion_detector() == 'Yes':
    #     st.write('Thanks for reaching out! I hope I\'ve been able to help you address your life insurance needs')
    #     conclusion_detection.json_extractor()
    # else:
    #     pass
    
    
