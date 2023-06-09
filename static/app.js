class Chatbox{
    constructor(){
        this.args={
            openButton: document.querySelector('.chatbox__button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button'),
        }
        this.state=false;
        this.message=[];
    }
    
    display(){
        const {openButton,chatBox,sendButton}=this.args;

        openButton.addEventListener('click',()=>this.toggleState(chatBox));

        sendButton.addEventListener('click',()=>this.onSendButton(chatBox));

        const node=chatBox.querySelector('input');
        node.addEventListener("keyup",({key})=>{
            if(key==='Enter') {
                this.onSendButton(chatBox);
                node.value = "";  //Clearing text box here after hitting enter
            }
        })
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