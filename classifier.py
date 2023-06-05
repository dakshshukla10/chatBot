import os
import openai
from dotenv import load_dotenv, find_dotenv
import json
_ = load_dotenv(find_dotenv())

openai.api_key = os.environ['OPENAI_API_KEY']


def getResponse(messages,model="gpt-3.5-turbo",temperature=0,max_tokens=500):
    response = openai.ChatCompletion.create(model=model,messages=messages,temperature=temperature,max_tokens=max_tokens,)
    return response.choices[0].message["content"]

def inputClassifier(inputText):  
    delimiter = "####"
    system_message = f"""
    You will be provided with customer queries. \
    The customer service query will be delimited with {delimiter} characters. \
    Classify each query into one of the following categories: \
    1) Customer is saying Hi or Bye. Classify it as ```greeting``` \
    2) Customer wants to know when their vehicle will be charged. Classify it as ```chargeCompletionTime``` \
    3) Customer wants to know why their vehicle is not charging. Classify it as ```notCharging``` \
    5) If it is not one of the above, classify it as ```newQuery```
    Provide your output in json format with the \
    keys: class
    """
    user_message = inputText
    messages = [
        {'role': 'system',
        'content': system_message},
        {'role': 'user',
        'content': f"{delimiter}{user_message}{delimiter}"},
    ]
    response = json.loads(getResponse(messages=messages))

    return response
