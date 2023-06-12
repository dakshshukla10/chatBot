import random 
import json

# Get recent message 
def getRecentMessage():

    # Define the file and learn instructions 
    fileName="storedData.json"
    
    # Initialize messages
    messages = []

    try:
        with open(fileName) as userFile:
            data = json.load(userFile)

            # Append the last 7 items of data 
            if data:
                if len(data) < 7:
                    for item in data:
                        messages.append(item)
                else:
                    for item in data[-7:]:
                        messages.append(item)        
    except Exception as e:
        print("Error in getRecentMessage",e)
        return None

    return messages 

# Store Messages 
def storeMessage(requestMessage,responseMessage):
    # Define the file name
    fileName="storedData.json"

    # Get recent messages from database
    messages = getRecentMessage() # Removing the system message

    # Append the new message to the data
    userMessage = {"role":"user","content":requestMessage}
    assistantMessage = {"role":"assistant","content":responseMessage}
    messages.append(userMessage)
    messages.append(assistantMessage)

    # Save the updated files 
    with open(fileName, 'w') as f:
        json.dump(messages, f)

# Reset Messages
def resetMessages():
    # overwrite current file with nothing  
    with open('storedData.json', 'w') as file:
        file.write("[]")

# Tests 
# print(getRecentMessage())
# resetMessages()
# storeMessage("Hi","Hello, how can I help you ?")
# print(getRecentMessage())