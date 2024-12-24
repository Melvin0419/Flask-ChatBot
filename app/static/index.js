async function sendMessage(){
    const userInput = document.getElementById('user-input');
    const message = userInput.value.trim();

    if(!message){
        alert("Please type a message!");
        return;
    }

    // Display user message
    const messagesDiv = document.getElementById('messages');
    const userMessageDiv = document.createElement('div');
    userMessageDiv.className = 'message user';
    userMessageDiv.textContent = message;
    messagesDiv.appendChild(userMessageDiv);

    // Clear input field
    userInput.value = '';

    // Send message to the server
    const response = await fetch('/chats',{
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body: JSON.stringify({message:message}),
    });

    const data = await response.json();

    // Display assistant's reply
    const assistantMessageDiv = document.createElement('div');
    assistantMessageDiv.className='message assistant';
    assistantMessageDiv.textContent = data.reply || 'Error:Unable to get a response.';
    messagesDiv.appendChild(assistantMessageDiv);

    // Scroll to the bottom of the chat
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

let isRecording = false;
let mediaRecorder;
let audioChunks = [];

async function toggleRecording(){
    const recordButton = document.getElementById('record-button')

    if(!isRecording){
        // Start recording
        isRecording = true;
        recordButton.textContent = 'Stop';
        audioChunks = [];

        try{
            const stream = await navigator.mediaDevices.getUserMedia({audio:true});
            mediaRecorder = new MediaRecorder(stream);

            mediaRecorder.ondataavailable = event => {
                if (event.data.size > 0){
                    audioChunks.push(event.data);
                }
            };

            mediaRecorder.start();
        } catch(error){
            console.error('Error accessing microphone:',error);
            isRecording = false;
            recordButton.textContent = 'Record';
        }
    } else {
        // Stop recording
        isRecording = false;
        recordButton.textContent = 'Record';

        mediaRecorder.stop();
        mediaRecorder.onstop = () => {
            const audioBlob = new Blob(audioChunks, {type:'audio/wav'});
            sendAudioToServer(audioBlob);
        };
    }
}

/**
 * Sends the recorded audio file to the server.
 * @param {Blob} audioBlob - The audio data to send.
 */

async function sendAudioToServer(audioBlob){
    const formData = new FormData();
    formData.append('audio',audioBlob);

    try {
        const response = await fetch('/chats',{
            method:'POST',
            body:formData,
        });

        const data = await response.json();
        if (data.reply){
            addMessage('Assistant',data.reply);
        }
    } catch (error) {
        console.error('Error sending audio to server:',error);
    }
}

/**
 * Adds a new message to the chat UI.
 * @param {string} sender - The sender of the message (e.g., "User" or "Assistant").
 * @param {string} text - The content of the message.
 */

function addMessage(sender, text){
    const messagesDiv = document.getElementById('messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message';
    messageDiv.textContent = `${sender}:${text}`;
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}