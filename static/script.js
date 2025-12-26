let lastBotReply = "";

// ---------------- WELCOME MESSAGE ----------------
window.onload = () => {
    addMessage("bot", "Hello! How can I help you today? 😊");
};

// ---------------- SEND MESSAGE ----------------
async function sendMessage() {
    const input = document.getElementById("userInput");
    const message = input.value.trim();
    if (!message) return;

    addMessage("user", message);
    input.value = "";

    const response = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message })
    });

    const data = await response.json();
    lastBotReply = data.reply;
    addMessage("bot", data.reply);
}

// ---------------- ADD MESSAGE ----------------
function addMessage(sender, text) {
    const chatBox = document.getElementById("chatBox");
    const msg = document.createElement("div");
    msg.className = sender;
    msg.innerText = text;
    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// ---------------- VOICE INPUT ----------------
function startVoice() {
    if (!('webkitSpeechRecognition' in window)) {
        alert("Speech Recognition not supported in this browser");
        return;
    }
    const recognition = new webkitSpeechRecognition();
    recognition.lang = "en-US";
    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.onresult = (event) => {
        const voiceText = event.results[0][0].transcript;
        document.getElementById("userInput").value = voiceText;
        sendMessage();
    };

    recognition.start();
}

// ---------------- TEXT TO SPEECH ----------------
function speakLast() {
    if (!lastBotReply) return;
    const speech = new SpeechSynthesisUtterance(lastBotReply);
    speech.lang = "en-US";
    window.speechSynthesis.speak(speech);
}
