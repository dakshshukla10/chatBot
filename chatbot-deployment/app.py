from flask import Flask, render_template, request,jsonify
from classifier import inputClassifier

app=Flask(__name__)

@app.get("/")
def index_get():
    return render_template('base.html')

@app.post("/response")
def response():
    inputText=request.get_json().get("message")
    # TODO Check if text is valid(empty)
    
    response = inputClassifier(inputText)
    message = {"answer":response}
    return jsonify(message)

if __name__=="__main__":
    app.run(debug=True)
