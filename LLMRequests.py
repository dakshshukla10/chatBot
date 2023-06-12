import os
import openai
from dotenv import load_dotenv, find_dotenv
import json
_ = load_dotenv(find_dotenv())

# Custom Function import
from database import getRecentMessage

# Retrieve API key from .env file
openai.api_key = os.environ['OPENAI_API_KEY']
openai.organization = os.environ['OPEN_AI_ORG']

def getResponse(messages,model="gpt-3.5-turbo",temperature=0,max_tokens=500):
    response = openai.ChatCompletion.create(model=model,messages=messages,temperature=temperature,max_tokens=max_tokens,)
    return response.choices[0].message["content"]

def greetingResponse(inputText):  
    delimiter = "####"
    system_message = f"""    
    You will be provided with customer queries. \
    The customer service query will be delimited with {delimiter} characters. \
    Classify each query into one of the following categories and return the respective response: \
    1) Greting , saying hi or hello. Return this string ```Hi, how can I help you today?``` \
    2) Saying bye. Return this string ```Bye now ;)``` \
    Provide your output in string format as mentioned above. \
    """
    userMessage = inputText
    messages = [
        {'role': 'system',
        'content': system_message},
        {'role': 'user',
        'content': f"{delimiter}{userMessage}{delimiter}"},
    ]
    response = str(getResponse(messages=messages))

    return response

def getResponseFromMessages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, 
    )
    return response.choices[0].message["content"]

# OpenAI - Wisper 
# Convert audio-to-text
def convertAudioToText(audioFile):
    try:
        
        transcript = openai.Audio.transcribe("whisper-1", file=audioFile,language="en") 
        messageText = transcript['text']
        return messageText
    except Exception as e:
        print("Error in audio-to-text conversion",e)
        return None