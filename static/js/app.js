class Chatbox{
    constructor(){
        this.args={
            openButton: document.querySelector('.chatbox__button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button')   
        }
        this.state = false;
        this.messages = [];
        this.checkup_ID='';
    }

    display(){
        const{openButton,chatBox,sendButton}=this.args;
        openButton.addEventListener('click',()=>this.toggleState(chatBox))
        sendButton.addEventListener('click', () => this.onSendButton(chatBox))
        const e_btn=chatBox.querySelector('input');
        e_btn.addEventListener("keypress",(event)=>{
            console.log(event);
            if(event.key === "Enter")
            {
                this.onSendButton(chatBox);
                console.log("enter pressed");
            }
              
        });
    }

    toggleState(chatbox){
        this.state=!this.state;
        if(this.state)
            chatbox.classList.add('chatbox--active');
        else
            chatbox.classList.remove('chatbox--active');
    }

    onSendButton(chatbox){
        var textField=chatbox.querySelector('input');
        let msg=textField.value;
        if(msg==="")
         return;
        let msg1={name:"user",message:msg}
        this.messages.push(msg1);
        fetch('http://127.0.0.1:8000/health/predict',{
              method: 'POST',
              body:JSON.stringify({message:msg,checkup_ID:this.checkup_ID}),
              mode:'cors',
              headers:{
                  'Content-Type':'application/json'
              },})
              .then(res=>res.json())
              .then(r=>{
                  console.log(r);
                  let msg2={name:"sam",checkup_ID:r.checkup_ID,message:r.reply};
                  this.messages.push(msg2);
                  this.checkup_ID=r.checkup_ID;
                  console.log(msg2);
                  this.updateChatText(chatbox)
                  textField.value='';
              }).catch((error)=>{
                  console.log('Error',error);
                  textField.value=''
              });

    }

    updateChatText(chatbox){
        var html='';
        var typing = '<div class="chat-bubble messages__item--typing">'+'<div class="typing">'+'<div class="dot"></div><div class="dot"></div><div class="dot"></div></div ></div >'
        this.messages.slice().reverse().forEach(function(item){
            if(item.name=="sam")
            {
                html+='<div class="messages__item messages_item--visitor">'+item.message+'</div>';
            }
            else
            {
                html += '<div class="messages__item messages__item--operator">' + item.message + '</div>';
            }

        });
        const chatmessage=chatbox.querySelector('.chatbox__messages');
        chatmessage.innerHTML = typing + chatmessage.innerHTML;
        setTimeout(() => {
            chatmessage.innerHTML = html;
        },1000);
        
    }
}
const chat=new Chatbox()
chat.display();