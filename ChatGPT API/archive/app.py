from flask import Flask, render_template, request
import openai
from openai import OpenAI
from langchain.chat_models import ChatOpenAI
import os


app = Flask(__name__)

# Set up OpenAI API credentials
# openai.api_key = os.getenv('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')


client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key="",
)

def chat_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response

chat_gpt('Hi')
# Define the default route to return the index.html file
@app.route("/")
def home():
    return render_template("index.html")

# Define the /api route to handle POST requests
@app.route("/api", methods=["POST"])
def api():
    # Get the message from the POST request
    message = request.json.get("message")
    # Send the message to OpenAI's API and receive the response
    
    response1 = chat_gpt(message)
    
    # completion = openai.ChatCompletion.create(
    # model="gpt-3.5-turbo",
    # messages=[
    #     {"role": "user", "content": message}
    # ]
    # )
    if response1.choices[0].message!=None:
        chat_dict = {
        'content':response1.choices[0].message.content,
        'role':response1.choices[0].message.role
        }
        print(chat_dict)
        
        return chat_dict#response1.choices[0].message.content

    else :
        return 'Failed to Generate response!'
    

if __name__=='__main__':
    app.run(debug=True)

