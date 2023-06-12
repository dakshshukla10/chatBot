import openai

from database import getRecentMessage

def getCompletionFromMessages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,  
    )
#     print(str(response.choices[0].message))
    return response.choices[0].message["content"]

def findContinuedConversation(messages):
    messages=getRecentMessage()
    if len(messages)>1 and messages[-1]=={"role": "assistant", "content": "Kindly provide the vehicle ID"}:
        print("Continuing conversation")
        return True,"The vehicle will finish charging at 10:00 PM"
    return False,""