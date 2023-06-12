from http.client import HTTPException
from flask import Flask, render_template, request,jsonify
import os
import requests
from LLMRequests import convertAudioToText

# Internal imports
from classifier import inputClassifier
from continueConversation import findContinuedConversation
from conversationFlow import conversation 

app=Flask(__name__)

@app.get("/")
def index_get():
    return render_template('base.html')

@app.post("/response")
def response():
    inputText = request.get_json().get("message")
    # TODO Check if text is valid(empty)
    
    continued = False

    # Check for continued conversation
    continued,response = findContinuedConversation(inputText)

    if not continued:
        # Classify input
        classifiedInput = inputClassifier(inputText)

        response = conversation(classifiedInput,inputText)
        print("Returned",response)

    
    message = {"answer":response}
    return jsonify(message)

@app.route('/fetchAudio', methods=['POST'])
def fetch_audio():
    inputAudio = request.files['audio']
    inputAudio.save(os.path.join("audioFiles", inputAudio.filename))
    return 'File uploaded and saved.', 200

@app.get("/processAudio")
def get_audio():
    print("Processing audio############################")
    # Get saved audio
    audioInput = open("audioFiles/recordedAudio.webm", "rb")

    # Decoded message
    message_decoded = convertAudioToText(audioInput)
    print("Decoded message",message_decoded)
    return message_decoded
    
    ############################################################################################################
    # # Guard: Ensure message decoded 
    # if not message_decoded:
    #     raise HTTPException(status_code=404, detail="Failed to decod audio")
    
    # # Get ChatGPT response)
    # url = 'http://127.0.0.1:8080/response'  # Replace with your Flask endpoint URL

    
    # # JSON payload
    # payload = message_decoded

    # chatResponse = requests.post(url, json=payload)

    # # Guard: Ensure received chat response
    # if not chatResponse:
    #     raise HTTPException(status_code=404, detail="Failed to get chat response")

    # return chatResponse
    ############################################################################################################


    # # Store messages 
    # store_message(message_decoded,chat_response)

    # # Convert text to speech
    # audio_output = convert_text_to_speech(chat_response)

    # # Guard: Ensure got audio back 
    # if not chat_response:
    #     raise HTTPException(status_code=404, detail="Failed to get Eleven Labs audio response")

    # # Create a generator yield chunk of data 
    # def iterfile():
    #     yield audio_output

    # return StreamingResponse(iterfile(), media_type="audio/mpeg")



if __name__=="__main__":
    app.run(port=8080,debug=True)
