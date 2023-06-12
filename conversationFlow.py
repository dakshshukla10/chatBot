import requests
import json

from LLMRequests import greetingResponse
from database import resetMessages, storeMessage

def conversation(classification,inputText):    
    if classification["class"] == "greeting":
        return greeting(inputText)
    elif classification["class"] == "notCharging":
        return vehicleChargingStatus(inputText)
    elif classification["class"] == "chargeCompletionTime":
        return vehicleChargeCompletionTime(inputText)
    else:
        return newQuery(inputText)

def greeting(input):
    response=greetingResponse(input)
    return response

def vehicleChargingStatus(input):
    return input

def vehicleChargeCompletionTime(input):
    response="Kindly provide the vehicle ID"
    storeMessage(input,response)
    return response

def newQuery(input):
    url = 'http://127.0.0.1:5000/chatbot/ask-ava'  # Replace with your Flask endpoint URL

    # JSON payload
    payload = {
        "question": input
    }

    response = requests.post(url, json=payload)
    
    if response:
        data = response.json()["answer"]
    else:
        print('Request failed with status code', response.status_code)
    return data