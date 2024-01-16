import os
import openai
from dotenv import load_dotenv

load_dotenv()

# Loading Environent Variables
api_type = os.environ.get('OPENAI_API_TYPE')
api_base = os.environ.get('OPENAI_API_BASE')
api_key = os.environ.get('OPENAI_API_KEY')
api_version = os.environ.get('OPENAI_API_VERSION')

# Set your OpenAI API key here
openai.api_type = api_type
openai.api_base = api_base
openai.api_key = api_key
openai.api_version = api_version



def response_generator(prompt_input):
    return openai.ChatCompletion.create(
    engine="gpt-35-turbo",
    messages = prompt_input,
    # model="gpt-3.5-turbo",
    max_tokens=800,
    top_p=0.95,
    frequency_penalty=0,
    presence_penalty=0,
    stop=None
)
