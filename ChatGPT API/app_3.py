# %load_ext autoreload
# %autoreload 2
from azure_response import response_generator
import streamlit as st
from conversation_conclusion import conclusion_processing
from system_message_appender import stage_controller
import re
import time

# st.write(st.session_state.stage_tracker)
# Display title and chat history
image_path = 'acko-logo-1920x1080.png'
st.sidebar.image(image_path, use_column_width=True)

# st.sidebar.header('Products')
# # st.sidebar.markdown('<a href="https://www.youtube.com/" target="_blank">Buy Auto Policy</a>', unsafe_allow_html=True)

# st.sidebar.markdown('<a href="https://www.youtube.com/" target="_blank" style="text-decoration: none; color: #008CBA; font-weight: bold; font-size: 18px;">Car</a>', unsafe_allow_html=True)
# st.sidebar.markdown('<a href="https://www.youtube.com/" target="_blank" style="text-decoration: none; color: #008CBA; font-weight: bold; font-size: 18px;">Bike</a>', unsafe_allow_html=True)
# st.sidebar.markdown('<a href="https://www.youtube.com/" target="_blank" style="text-decoration: none; color: #008CBA; font-weight: bold; font-size: 18px;">Health</a>', unsafe_allow_html=True)
# st.sidebar.markdown('<a href="https://www.youtube.com/" target="_blank" style="text-decoration: none; color: #008CBA; font-weight: bold; font-size: 18px;">Travel</a>', unsafe_allow_html=True)
# st.sidebar.markdown('<a href="https://www.youtube.com/" target="_blank" style="text-decoration: none; color: #008CBA; font-weight: bold; font-size: 18px;">Corporate Coverage</a>', unsafe_allow_html=True)
# st.sidebar.markdown('<a href="https://www.youtube.com/" target="_blank" style="text-decoration: none; color: #008CBA; font-weight: bold; font-size: 18px;">Electronics</a>', unsafe_allow_html=True)

st.sidebar.header('Attachments')
uploaded_file = st.sidebar.file_uploader("Upload file", type=["pdf", "txt", "csv"])


# # st.sidebar.subheader('Additional Information')

# additional_text_1 = '<a href="https://www.acko.com/contact-us/" target="_blank" style="text-decoration: none; color: #008CBA; font-size: 12px;">Contact Us</a>'
# additional_text_2 = '<a href="https://www.acko.com/customer-service/" target="_blank" style="text-decoration: none; color: #008CBA; font-size: 12px;">Customer Service</a>'
# additional_text_3 = '<a href="https://www.acko.com/terms-and-conditions/" target="_blank" style="text-decoration: none; color: #008CBA; font-size: 12px;">Terms and Conditions</a>'

# st.sidebar.markdown(f'{additional_text_1}<br>{additional_text_2}<br>{additional_text_3}', unsafe_allow_html=True)
# Define links for different pages
# if st.sidebar.button('Page 1'):
#     # Redirect to an external website when "Page 1" is clicked
#     st.markdown("[Go to External Website](https://www.youtube.com/)")
# elif st.sidebar.button('Page 2'):
#     # Add functionality for Page 2 if needed
#     st.write("Content for Page 2")
# elif st.sidebar.button('Back to Home'):
#     # Add functionality for Page 2 if needed
#     st.write("Content for Page 2")


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

def submit():
    st.session_state.something = st.session_state.user_input1
    st.session_state.user_input1 = ''
    return st.session_state.something


# Progress bar - Not useful right now    
# def simulate_task(progress):
#     progress_bar = st.progress(progress)  # Initialize progress bar
#     progress_bar.progress(progress)
#     # for i in range(100):
#     #     # Update the progress bar value
#     #     progress_bar.progress(i + 1)
#     #     time.sleep(0.1)  # Simulating a delay

# def simulate_task_2():
#     st.write('<style>div.Widget.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
#     progress_bar = st.progress(0)

#     # List of checkpoint names
#     checkpoints = ["Checkpoint 1", "Checkpoint 2", "Checkpoint 3", "Checkpoint 4", "Checkpoint 5", "Checkpoint 6"]

#     for i in range(len(checkpoints)):
#         st.write(f'<div style="position:relative;width:100%;">\
#                     <div style="position:absolute;text-align:center;left:{i*16.5}%;transform:translate(-50%);width:100px;">{checkpoints[i]}</div>\
#                  </div>', unsafe_allow_html=True)
#         progress_bar.progress((i + 1) * 16.67)

# Submit variable
if 'something' not in st.session_state:
    st.session_state.something = ''

# Initialize Progress
if 'progress_tracker' not in st.session_state:
    st.session_state.progress_tracker = 0


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
        # st.write(st.session_state.current_stage)
    except:
        st.session_state.current_stage = 0


# Related to progress bar
# st.session_state.progress_tracker += 1
# simulate_task(st.session_state.progress_tracker)  


if (st.session_state.stage_tracker == 1) & (int(st.session_state.current_stage) <= 5):
    stage_initiation = stage_controller(st.session_state.conversation_history, '',5)
    st.session_state.stage_data = stage_initiation.json_reader(int(st.session_state.current_stage))


# User input and sending messages

user_input = st.text_input("Type a message...", key="user_input1", on_change=submit)
user_input = st.session_state.something
if user_input:  
    # simulate_task_2()
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
        # st.write(stage)
    else:
        st.session_state.stage_tracker = stage
        # st.write(stage)
        # st.write(st.session_state.current_stage)
        # conv_end = 'No'
    
    # simulate_task()
    

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
    
    
