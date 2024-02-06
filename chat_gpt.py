from copyreg import constructor
import openai

OPENAI_ORG_ID = 'org-yM6MbuKD6qh8UR63H72ljeG1'
OPENAI_API_KEY = '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'

openai.organization = OPENAI_ORG_ID
openai.api_key = OPENAI_API_KEY

def get_gpt_response(messages,functions):
    if functions is not None:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=messages,
            functions=functions,
            function_call="auto",
        )
        return response
    else:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=messages,
        )
        return response
    
messages = [
    {"role": "user", "content": "Hi What can you do for me"}
]

res = get_gpt_response(messages,None)
print(res)