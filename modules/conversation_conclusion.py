from modules.azure_response import response_generator
import openai
import requests
import json

class conclusion_processing():
    def __init__(self, base_file):
        self.base_file = base_file

    # Function to generate a response using ChatGPT API

    def conclusion_detector(self):
        conclusion_query = self.base_file
        conclusion_query.append({'role':'user','content':'Does it look it the conversation has reached it\'s conclusion? Please answer in Yes or No'})
        response = response_generator(conclusion_query)['choices'][0]['message']['content']
        if 'yes' in str.lower(response):
            return 'Yes'
        else:
            return 'No'
        
    def json_extractor(self):
        conclusion_query = self.base_file
        conclusion_query.append({'role':'user','content':"Give me all the data collected for this user in a Json Format. Format should be following and no other text - 'variable':'value'"})
        response = response_generator(conclusion_query)['choices'][0]['message']['content']
        with open('json_data.txt','w') as f:
            json.dump(response, f)

