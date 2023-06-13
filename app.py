from http.client import HTTPException
from flask import Flask, render_template, request,jsonify,Response,stream_with_context
import os
import requests
from LLMRequests import convertAudioToText

# Internal imports
from classifier import inputClassifier
from continueConversation import findContinuedConversation
from conversationFlow import conversation
from textToSpeach import convertTextToSpeech 

app=Flask(__name__)

@app.get("/")
def index_get():
    return render_template('base.html')

@app.post("/response")
def response():
    inputText = request.get_json().get("message")
    # TODO Check if text is valid(empty)
    
    print("Request",request.get_json())
    continued = False

    # Check for continued conversation
    continued,response = findContinuedConversation(inputText)

    if not continued:
        # Classify input
        classifiedInput = inputClassifier(inputText)

        response = conversation(classifiedInput,inputText)

    audio=convertTextToSpeech(response)
    message = {"answer":response}
    return jsonify(message)

@app.route('/fetchAudio', methods=['POST'])
def fetch_audio():
    inputAudio = request.files['audio']
    inputAudio.save(os.path.join("audioFiles", inputAudio.filename))
    return 'File uploaded and saved.', 200

@app.get("/processAudio")
def getAudio():
    # Get saved audio
    audioInput = open("audioFiles/recordedAudio.webm", "rb")

    # Decoded message
    message_decoded = convertAudioToText(audioInput)
    result={"message":message_decoded,"status": 200}
    return jsonify(result)

@app.route('/textToSpeach', methods=['POST'])
def textToSpeach():
    inputText = request.get_json().get("message")  
    audioOutput=convertTextToSpeech(inputText)

    # Create a generator that yields chunks of data
    def generate_audio():
        yield audioOutput    

    # Use for POST: Return output audio
    return Response(stream_with_context(generate_audio()), mimetype="application/octet-stream")



if __name__=="__main__":
    app.run(port=8080,debug=True)
