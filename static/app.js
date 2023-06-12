
class Chatbox{
    constructor(){
        this.args={
            openButton: document.querySelector('.chatbox__button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button'),
            recordButton: document.getElementById('recordButton')
        }
        this.state=false;
        this.message=[];
        this.mediaRecorder = null;
        this.audioChunks = [];
    }
    
    display(){
        const {openButton,chatBox,sendButton,recordButton}=this.args;

        openButton.addEventListener('click',()=>this.toggleState(chatBox));

        sendButton.addEventListener('click',()=>this.onSendButton(chatBox));

        recordButton.addEventListener('click', () => {
            if (recordButton.textContent === 'Start') {
                this.startRecording();
            } else {
                this.stopRecording();
            }
        });

        const node=chatBox.querySelector('input');
        node.addEventListener("keyup",({key})=>{
            if(key==='Enter') {
                this.onSendButton(chatBox);
                node.value = "";  //Clearing text box here after hitting enter
            }
        })
    }

    startRecording() {
        this.audioChunks = [];
        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(stream => {
                this.mediaRecorder = new MediaRecorder(stream);
                this.mediaRecorder.start();
                
                this.mediaRecorder.addEventListener("dataavailable", event => {
                    this.audioChunks.push(event.data);
                });
                
                this.args.recordButton.textContent = 'Stop';
            }).catch(error => console.error(error));
    }

    stopRecording() {
        this.mediaRecorder.stop();
        // To use the 'this' reference in the callback function
        const that = this;  // Save the 'this' reference
        this.mediaRecorder.stop();

        this.mediaRecorder.addEventListener("stop", () => {
            const audioBlob = new Blob(this.audioChunks);
            const formData = new FormData();
            formData.append('audio', audioBlob, 'recordedAudio.webm');
            
            fetch('http://127.0.0.1:8080/fetchAudio', {
                method: 'POST',
                body: formData
            }).then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                console.log('Audio data sent successfully',response);
            }).catch(error => console.error(error))
            .then(() => {
            return fetch('http://127.0.0.1:8080/processAudio');
                })
                .then(response => {
                    console.log("First Response point",response)
                    if (response.status!=200) {
                        throw new Error('Network response was not ok');
                    }
                    console.log('Audio data processed successfully',response);
                    return response.json(); 
                }).catch(error => console.error(error))
                .then(inputMessage => {console.log(inputMessage['message']);
                    that.onSendAudio(inputMessage, that.args.chatBox)})
            }    
        );
        
        // fetch('http://127.0.0.1:8080/processAudio')
        //     .then(response => {
        //         if (!response.ok) {
        //         throw new Error('Network response was not ok');
        //         }
        //         console.log('Audio data sent successfully');
        //     })
        //     .catch(error => console.error(error));

        this.args.recordButton.textContent = 'Start';

    }

    toggleState(chatBox){
        this.state=!this.state;

        //show or hide the box
        if(this.state){
            chatBox.classList.add('chatbox--active');
        }else{
            chatBox.classList.remove('chatbox--active');
        }
    }

    onSendButton(chatBox){
      var textField = chatBox.querySelector("input");
      let text1 = textField.value;
      if (text1 === "") {
        return;
      }
      let msg1 = { name: "User", message: text1 };
      this.message.push(msg1);
      this.updateChatText(chatBox);
      textField.value = "";  //Clearing text box here after sending message

      // 'http://127.0.0.1:5000/response'
      fetch($SCRIPT_ROOT + "/response", {
        method: "POST",
        body: JSON.stringify({ message: text1 }),
        mode: "cors",
        headers: {
          "Content-Type": "application/json",
        },
      })
        .then((r) => r.json())
        .then((r) => {
        //   let msg2 = { name: "Sam", message: '<img src="/static/images/loader.gif" alt="Loading..." />' };
        //   this.message.push(msg2);
        //   this.updateChatText(chatBox);
          let msg3 = { name: "Sam", message: r.answer };
          this.message.push(msg3);
          this.updateChatText(chatBox);
          textField.value = "";
        })
        .catch((error) => {
          console.log("Error:", error);
          this.updateChatText(chatBox);
          textField.value = "";
        });
    }

    onSendAudio(inputMessage, chatBox){
      console.log("This has been reached",inputMessage)  
      let text1 = inputMessage["message"];
      
      if (text1 === "") {
        return;
      }
      let msg1 = { name: "User", message: text1 };
      this.message.push(msg1);

      // 'http://127.0.0.1:5000/response'
      fetch($SCRIPT_ROOT + "/response", {
        method: "POST",
        body: JSON.stringify({ message: text1 }),
        mode: "cors",
        headers: {
          "Content-Type": "application/json",
        },
      })
        .then((r) => r.json())
        .then((r) => {
          let msg3 = { name: "Sam", message: r.answer };
          this.message.push(msg3);
          this.updateChatText(chatBox);
        })
        .catch((error) => {
          console.log("Error:", error);
          this.updateChatText(chatBox);
        });
    }

    updateChatText(chatBox){
        var html="";
        this.message.slice().reverse().forEach(function(item,index){
            if(item.name==="Sam"){
                html+=`<div class="messages__item messages__item--visitor">`+item.message+`</div>`;
            }
            else{
                html+=`<div class="messages__item messages__item--operator">`+item.message+`</div>`;
            }

            const chatmessage=chatBox.querySelector('.chatbox__messages');
            chatmessage.innerHTML=html;
        })
    }
}

const chatbox=new Chatbox();
chatbox.display();