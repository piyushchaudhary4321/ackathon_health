def info_retrieve(info=None):
    # called without parameters it returns the required openai template.
    if info==None:
        return {
    "name": "initial_file", "description": "Get the following information from a user", 
    "parameters": { 
        "type": "object", 
        "properties": { "age": { "type": "int", "description": "What is your age" },
                        "income": { "type": "int", "description": "What is your income level" },
                        "diabetes_flag": { "type": "str", "description": "Do you have diabetes(Yes/No)" }
                        }
    },
    "required" : ["age", "income", "diabetes_flag"]
}

