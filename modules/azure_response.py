import openai

# Set your OpenAI API key here
openai.api_type = "azure"
openai.api_base = "https://ackocare4.openai.azure.com/"
# openai.api_version = "2023-07-01-preview"
openai.api_key = '85fe299e16cc403098fcfe69fe4877ce'
openai.api_version = "2023-08-01-preview"



def response_generator(prompt_input):
    return openai.ChatCompletion.create(
    engine="AckoCareLife2",
    messages = prompt_input,
    # model="gpt-3.5-turbo",
    max_tokens=800,
    top_p=0.95,
    frequency_penalty=0,
    presence_penalty=0,
    stop=None
)
