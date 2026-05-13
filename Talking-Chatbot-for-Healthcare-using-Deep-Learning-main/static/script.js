const chatBox = document.getElementById('chat-box');
const textInput = document.getElementById('text-input');
const sendBtn = document.getElementById('send-btn');
const micBtn = document.getElementById('mic-btn');
const recordingIndicator = document.getElementById('recording-indicator');

// Setup Speech Synthesis for Bot Voice
const synth = window.speechSynthesis;
let botVoice = null;

// Wait for voices to load
if ('onvoiceschanged' in synth) {
    synth.onvoiceschanged = () => {
        const voices = synth.getVoices();
        botVoice = voices.find(v => v.lang.includes('en') && v.name.includes('Female')) || voices[0];
    };
}

function speak(text) {
    if (synth.speaking) synth.cancel(); // Stop current speech
    const utterThis = new SpeechSynthesisUtterance(text);
    if (botVoice) utterThis.voice = botVoice;
    utterThis.pitch = 1.1;
    utterThis.rate = 1.0;
    synth.speak(utterThis);
}

// Browser Autoplay Policy: We must wait for the user to click the page before speaking.
let hasGreeted = false;
document.body.addEventListener('click', () => {
    if (!hasGreeted && botVoice) {
        speak("Hello! I am your AI healthcare assistant. Please tell me your symptoms.");
        hasGreeted = true;
    }
}, { once: true });

// Setup Speech Recognition
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
if(!SpeechRecognition) {
    alert("Speech Recognition API is not supported in this browser. Please use Chrome.");
} else {
    const recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.lang = 'en-US';
    recognition.interimResults = false;

    // Handle Mic Button (Click to toggle listening)
    let isListening = false;

    micBtn.addEventListener('click', (e) => {
        e.preventDefault();
        if(!isListening) {
            try {
                recognition.start();
                micBtn.classList.add('listening');
                recordingIndicator.classList.remove('hidden');
                isListening = true;
            } catch(err) {} 
        } else {
            recognition.stop();
            micBtn.classList.remove('listening');
            recordingIndicator.classList.add('hidden');
            isListening = false;
        }
    });

    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        micBtn.classList.remove('listening');
        recordingIndicator.classList.add('hidden');
        isListening = false;
        
        appendMessage(transcript, 'user');
        fetchResponse(transcript);
    };

    recognition.onerror = (event) => {
        micBtn.classList.remove('listening');
        recordingIndicator.classList.add('hidden');
        isListening = false;
        if(event.error !== 'no-speech') {
            console.log("Speech Error: " + event.error);
        }
    };
    
    recognition.onend = () => {
        micBtn.classList.remove('listening');
        recordingIndicator.classList.add('hidden');
        isListening = false;
    };
}

// Handle Text Submit
sendBtn.addEventListener('click', () => {
    const msg = textInput.value.trim();
    if(msg) {
        appendMessage(msg, 'user');
        fetchResponse(msg);
        textInput.value = '';
    }
});

textInput.addEventListener('keypress', (e) => {
    if(e.key === 'Enter') sendBtn.click();
});

function appendMessage(text, sender) {
    const msgDiv = document.createElement('div');
    msgDiv.classList.add('message', sender === 'user' ? 'user-message' : 'bot-message');
    
    msgDiv.innerHTML = `
        <div class="message-content">
            <p>${text}</p>
        </div>
    `;
    
    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

async function fetchResponse(message) {
    const typingId = 'typing-' + Date.now();
    const typingDiv = document.createElement('div');
    typingDiv.classList.add('message', 'bot-message');
    typingDiv.id = typingId;
    typingDiv.innerHTML = `<div class="message-content"><p>...</p></div>`;
    chatBox.appendChild(typingDiv);
    chatBox.scrollTop = chatBox.scrollHeight;

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: message })
        });
        const data = await response.json();
        
        document.getElementById(typingId).remove();
        
        appendMessage(data.reply, 'bot');
        speak(data.reply);

    } catch (error) {
        document.getElementById(typingId).remove();
        appendMessage("Server offline or disconnected.", 'bot');
    }
}
