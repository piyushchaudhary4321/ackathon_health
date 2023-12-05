

import os
import openai

openai.api_type = "azure"
openai.api_base = "https://ackocare4.openai.azure.com/"
openai.api_version = "2023-07-01-preview"
openai.api_key = '85fe299e16cc403098fcfe69fe4877ce'
# message_text = [{"role":"system","content":"You are AckoCares, an adept insurance advisor at Acko Life Insurance. Your approach involves guiding customers efficiently through the policy purchasing process with ease and clarity. To facilitate this, ask one question at a time on key topics like KYC information, financial needs, physical risk factors, medical history, and lab selection for tests. After each question, offer 2-4 examples of possible responses or points to clarify details, but do this selectively to avoid overwhelming the customer. This method aims to simplify the customer's decision-making process, making it easier for them to respond without overthinking. Continue to emphasize flexibility in the process, allowing customers to pause and resume as needed, and accept document submissions via email or photos. Your interactions should be straightforward and reassuring, focusing on customer convenience and understanding."}]
message_text = [{"role":"system","content":"Hi."}]
completion = openai.ChatCompletion.create(
  engine="AckoCareLife2",
  messages = message_text,
  temperature=0.7,
  max_tokens=800,
  top_p=0.95,
  frequency_penalty=0,
  presence_penalty=0,
  stop=None
)
completion
completion['choices'][0]['message']['content']
# New

# https://ackocare4.openai.azure.com/openai/deployments/AckoCareLife2/chat/completions?api-version=2023-07-01-preview

# 85fe299e16cc403098fcfe69fe4877ce

# from doten
openai.api_key = "1e312aee735446d196382ebd49213641"
openai.api_version = "2023-07-01-preview"
openai.api_type = "azure"
openai.api_base = "https://chatbot-acko.openai.azure.com/"

openai.api_type = "azure"
openai.api_base = "https://ackocarelife.openai.azure.com/openai/deployments/AckoCare/chat/completions?api-version=2023-07-01-preview"
openai.api_version = "2023-07-01-preview"
openai.api_key = "b55918bf404146ebb6c6f22915d729e8"

message_text = [{"role":"system","content":"You are a helpful Chat assistant of Acko Life Insurance company. You are required to help the user navigate through the key data points for insurance policy purchase journey, covering the steps mentioned below. Do this only one step at a time. Ask for information related to these activities that can cause physical injury 1) Occupation 2) Hobbies, 3) Travel, 4)Medical. Use short and sweet messages to communicate."}]
completion = openai.ChatCompletion.create(
  engine="AckoCare",
  messages = message_text,
  temperature=0.7,
  max_tokens=800,
  top_p=0.95,
  frequency_penalty=0,
  presence_penalty=0,
  stop=None
)