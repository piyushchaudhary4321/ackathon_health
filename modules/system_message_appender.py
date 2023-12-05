from modules.azure_response import response_generator
import pandas as pd
import os
import json

class stage_controller():
    def __init__(self, conv_history, messages,stage_json):
        self.conv_history = conv_history
        self.messages = messages
        # self.pitching_json = ["Explain that a good Life policy helps you with the following scenarios","Lockin Low Prices","Scale-up your Insurance coverage as Family grows","Increase Coverage if you buy a new house","Decrease the coverage when loan is paid off"]
        self.buy_journey = [
    {
        "Step Number": "0",
        "Name of the sheet": "Buy Journey",
        "Definition of Stage": "This stage involves collecting information from the user in order to recommend a suitable life insurance plan. Then it should calculate the price for the policy using the provided data.",
        "Closing Criteria for stage": "The user gets a price for the insurance policy desired."
    },
    {
        "Step Number": "1",
        "Name of the sheet": "Final Questionnaire Occupation",
        "Definition of Stage": "This stage is to understand if the Users Occupation has any Physical risks",
        "Closing Criteria for stage": "No specific risks found in this stage."
    },
    {
        "Step Number": "2",
        "Name of the sheet": "Final Questionnaire Hobbies",
        "Definition of Stage": "This stage is to understand if the Users Hobbies have any Physical risks",
        "Closing Criteria for stage": "No specific risks found.."
    },
    {
        "Step Number": "3",
        "Name of the sheet": "Final Questionnaire Travel",
        "Definition of Stage": "This stage is to understand if the Users International Travel history any Physical risks",
        "Closing Criteria for stage": "No specific risks found. Ask for more details if any risks are found."
    },
    {
        "Step Number": "4",
        "Name of the sheet": "VMER Questions",
        "Definition of Stage": "This stage involves collection of details of the user health history",
        "Closing Criteria for stage": "Collecting medical risk details of the customer, and no major risks identified which can lead to Rejection of proposal"
    },
    {
        "Step Number": "5",
        "Name of the sheet": "Mandatory data required checklist",
        "Definition of Stage": "This stage involves asking for information that is not covered in the conversation so far",
        "Closing Criteria for stage": "Check if most of the questions in this sheet have been answered in previous steps. Summarize if any data points are missed."
    },
    {
        "Step Number": "6",
        "Name of the sheet": "Closure and Next steps",
        "Definition of Stage": "This step involves telling the User if there are any negative findings that need to be addressed in detail later. If not tell the user that the process is completed, mention any pending steps",
        "Closing Criteria for stage": "Generate Draft policy PDF file using the generated JSON"
    },
    {
        "Step Number": "7",
        "Name of the sheet": "Conversation Close",
        "Definition of Stage": "This stage involves the user telling us that he is not interested in our offerings and is not interested in continuing the conversation",
        "Closing Criteria for stage": "User is not interested in the policy and the conversation needs to be terminated"
    }
]
        self.rejection_instructions = """Rejection Criteria: Reject if Total annual income is less than 10,00,000. Reject if the User is a politically exposed person (PEP). Reject if the User has been convicted of a criminal charges? Reject if the User if frequency involved in High risk Occupation frequently or Housewife or Student. Reject if Age less than 22 or more than 60. Reject if the user has suffered or been diagnosed or been treated for any of the terminal conditions like Cancer.

Only give the following reasons for rejection to the customer in a polite manner:
Risk associated with your occupation
Risk associated with your health
Due to involvement in risky adventure activities
Financial not suitable for policy
Incomplete details provided
Non availability of required information
Non completion of required application process
"""
        self.step_list = [i['Step Number'] for i in self.buy_journey]
        self.def_list = [i['Definition of Stage'] for i in self.buy_journey]
        self.step_json = dict(zip(self.step_list,self.def_list))
        self.base_pitch = "You are AckoCares, an adept insurance advisor at Acko Life Insurance. Your approach involves guiding customers efficiently through the policy purchasing process with ease and clarity. To facilitate this, ask one question at a time. After each question, offer 1 to 3 examples of possible responses, but do this selectively to avoid overwhelming the customer. This method aims to simplify the customer's decision-making process, making it easier for them to respond without overthinking. Mention about flexibility in the process once in awhile, allowing customers to pause and resume. Tell customer that they can also submit document via email or photos, if evidence submission is required in the process. Your interactions should be straightforward, focusing on customer understanding. Don't say Thank you to the user unnecessarily. "+ f"There are 8 stages involved in the life insurance purchase process, as defined in this json {self.step_json}. The same json has the criteria to move to the next stage that you should try to achieve through the conversation. The nature of the information to be requested varies according to the stage the user is at. In this json, the key step number defines the stage. Also, you need to reject policy issuance for a customer if the responses provided by them match the criteria in {self.rejection_instructions}. Note that resquest the user for a response in less than 50 words"
        self.stage_json = stage_json,
        # self.stage_change_flag = stage_change_flag
        self.stage0_instructions = """Introduce Acko Life insurance and explain that a Acko’s life insurance plan helps you to Lockin the Low Premium, Scale-up your Insurance coverage as Family grows, Increase Coverage if you buy a new house, Decrease the coverage when loan is paid off. It also offers riders to take care of drastic health situation leading to complete loss of income.


Collect below information from the customer and recommend a sum assured and Term for the Term life insurance policy 

Name
Age
Gender
Dependant Family members :  Spouse, Kids, Parents, Parent-in-laws
Average Monthly Income from all sources
Financial Goals in next 20 years : Buying house, higher education for kids, health coverage for aging parents

Check if the User is interested in buying the recommended plan or wants to change Sum assured or Term of plan or add the riders. Riders available are critical illness and permanent disability covers to take care of health expenses in case of any abrupt income loss event.

Gate criteria for Policy denial
These are go or no-go criteria to say whether we want to even evaluate a customer for Acko life insurance. Customers not meeting these criteria will be auto declined in the journey. 

Key parameters used for this evaluation are as follows, ask if the same is not available in conversation history :
Income
Education
Occupation
Location (pincode)
Politically exposed person (PEP)
Financial Sum at Risk (FSAR) = Sum Assured that Users wants

If DRC risk category is Preferred or Standard



FSAR <= 50 Lac
FSAR > 50 Lac
Education
>= Graduate
< Graduate
>= Graduate
= HSC
< HSC
Income (salaried)
 >= 2.5 Lac
>= 5 Lac
>= 4 Lac
>= 5 Lac
>= 10 Lac
Income (self employed)
>= 4 Lac
>= 5 Lac
>= 5 Lac
>= 5 Lac
>= 10 Lac



If DRC risk category is Medium or High

FSAR <= 50 lacs, min income required is 5 lacs
FSAR > 50 lacs, min income required is 10 lacs
Above limits are irrespective of education or occupation

*SSC is same as 10th Grade
**HSC is same 12th Grade

Min SSC education is required in any scenario. Below SSC will be rejected
All locations will be allowed initially. But system should have option to restrict basis pincode
Students/ Pensioners/ Agriculturist/Housewife/unemployed will be auto declined in phase 1 but can be offered insurance later on.


Reason for rejection that can be given to the customer are mentioned below:
Risk associated with your occupation
Risk associated with your health
Due to involvement in risky adventure activities
Financial not suitable for policy
Incomplete details provided
Non availability of required information
Non completion of required application process
"""
        self.stage1_instructions = """This stage is to understand if the User’s Occupation has any Physical risks. If the occupation given by the user is marked in the STP column as “No”, ask for more details as mentioned in the other columns for the same row.
"""
        self.stage2_instructions = """This stage is to understand if the User’s Hobbies have any Physical risks. If the Hobbies given by the user is marked in the STP column as “No”, ask for more details as mentioned in the other columns for the same row.
"""
        self.stage3_instructions = """This stage is to understand if the User’s International Travel history has any Physical risks If the International Travel History given by the user is marked in the STP column as “No”, ask for more details as mentioned in the other columns for the same row.
"""
        self.stage4_instructions = """This stage involves collection of details of the user's health status and history of any conditions. Collecting the medical risk details of the customer as per the questions mentioned in the “Questions” column. Use the data in “Values” column to inform the user about respond in these units. Once most of the information is collected, check if there are any major or serious risks identified which can lead to Rejection of a proposal. If Major risk are found Reject the policy
"""
        self.stage5_instructions = """This stage involves asking for information that is not covered in the conversation so far. Check if most of the questions given in this sheet have been answered in the conversation so far. Summarize if any data points are missed, and ask the user about it.
"""
        self.stage6_instructions = """This step involves telling the User if there are any negative findings that need to be addressed in detail later. If not, tell the user that the process is completed, and mention any pending data required. Generate Draft policy PDF file using the generated JSON
"""
        self.stage7_instructions = """Conclude Conversation
"""
        
        # self.stage0 = 'Introduce Acko Life insurance and explain that a Acko’s life insurance plan helps you to Lockin the Low Premium, Scale-up your Insurance coverage as Family grows, Increase Coverage if you buy a new house, Decrease the coverage when loan is paid off. It also offers riders to take care of drastic health situation leading to complete loss of income. '



    def stage_complete_detector(self):
        query_prompt = self.messages
        query_prompt.append({'role':'user','content':"1. Give me the output 1 if the user has reached the end of the current stage questioning else give the output 0. 2. Also give me a Yes/No answer on whether the conversation can't move further - either because the user is not interested in the product or the user has completed all prompts. Give me these 2 outputs as 2 variables in a json ['stage/conversation_end':value]. I just need these 2 variables in the specified format and no other text"})
        user_stage = response_generator(query_prompt)['choices'][0]['message']['content']
        return user_stage
    
    def json_reader(self,stage_num):
        for file in [i for i in os.listdir() if 'Stage' in i]:
            if str(stage_num) in file:
                with open(file, 'r') as file_import:
                    stage_data = json.load(file_import)        
        return stage_data

    def stage_change_processor(self):
        pass
