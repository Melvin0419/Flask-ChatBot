async function sendMessage(){
    const userInput = document.getElementById('user-input');
    const message = userInput.value.trim();

    if(!message){
        alert("Please type a message!");
        return;
    }

    // Display user message
    addMessage('user',message);

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
    addMessage('assistant',data.reply);
}

let recorder, audioContext
let isRecording = false;

async function toggleRecording(){
    const recordButton = document.getElementById('record-button');

    if(!isRecording){
        isRecording = true;
        recordButton.textContent = 'Stop';
        recordButton.className = 'clicked'
        
        try{
            // request microphone access
            const stream = await navigator.mediaDevices.getUserMedia({audio:true});
            // AudioContext: provides an environment for managing and processing audio in the browser 
            audioContext = new(window.AudioContext || window.webkitAudioContext)();
            // Connect mircophone's audio stream to the AudioContext
            const input = audioContext.createMediaStreamSource(stream);
            // Pass the audio sourse to Recorder.js to prepare for recording
            recorder = new Recorder(input);
            // Begin capturing audio
            recorder.record();
        } catch (error){
            console.error('error accessing microphone',error);
            isRecording = false;

            recordButton.textContent = 'Record';
            recordButton.className = 'unclick'
        }
    } else {
        isRecording = false;
        recordButton.textContent = 'Record';
        recordButton.className = 'unclick'
        // Stop recording 
        recorder.stop();
        // Retrieve the recorded audio as a Blob in WAV format and Send to the server
        recorder.exportWAV(async (blob) => {
            sendAudioToServer(blob);
        });
    }
}

async function sendAudioToServer(audioBlob){
    const formData = new FormData();
    formData.append('audio',audioBlob);
    try {
        const response = await fetch('/chats', {
            method: 'POST',
            body: formData,
        });

        const data = await response.json();

        if (data.reply) {
            addMessage('user', data.user_message);
            addMessage('assistant', data.reply);
        }
    } catch (error) {
        console.error('Error sending audio to server:', error);
    }
}

function addMessage(sender, text){
    const messagesDiv = document.getElementById('messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    messageDiv.textContent = text;
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}