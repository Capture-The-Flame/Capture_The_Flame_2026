
def get_chat_scripts():
    return f"""
<script>
const button = document.getElementById('recordBtn');
const userInput = document.getElementById('userInput');
const messages = document.getElementById('messages');
const sendBtn = document.querySelector('.sendBtn');

let conversation=[];

function addMessage(text, sender="user") {{
    const msg = document.createElement('div');
    msg.textContent = text;
    msg.classList.add('message', sender); 
    messages.appendChild(msg);
    messages.scrollTop = messages.scrollHeight;

    if(sender==="user"){{role="user";}}else{{role="assistant";}}
    conversation.push({{ role: role, content: text }});
}}

async function typeToGnome(message) {{
    if (!message.trim()) return;
    
    addMessage(message, "user"); // show user message
    userInput.value = "";

    try {{
        const response = await fetch('/typeToGnome', {{
            method: 'POST',
            headers: {{ 'Content-Type': 'application/json' }},
            body: JSON.stringify({{ message: message,history: conversation}})
        }});
        const data = await response.json();
        console.lo
        if (data['messages']) {{
            addMessage(data['messages'][0]['reply'], "gnome");
            const audioBytes = atob(data['messages'][1]['audio']);
                    const audioArray = new Uint8Array(audioBytes.length);
                    for (let i = 0; i < audioBytes.length; i++) {{
                        audioArray[i] = audioBytes.charCodeAt(i);
                    }}
                    const audioBlob = new Blob([audioArray], {{ type: "audio/wav" }});
                    const audioUrl = URL.createObjectURL(audioBlob);

                    // Play audio
                    const audio = new Audio(audioUrl);
                    audio.play();
        }}
    }} catch (err) {{
        addMessage("Error sending message", "gnome");
    }}
}}

sendBtn.addEventListener('click', () => {{
    typeToGnome(userInput.value);
}});

button.addEventListener('click', async () => {{
    try {{
        const stream = await navigator.mediaDevices.getUserMedia({{ audio: true }});
        const recorder = new MediaRecorder(stream);
        const chunks = [];

        // Show recording status in input
        userInput.value = "Recording in progress...";
        userInput.disabled = true;

        recorder.ondataavailable = e => chunks.push(e.data);
        recorder.onstop = async () => {{
            const blob = new Blob(chunks, {{ type: 'audio/webm' }});
            const formData = new FormData();
            formData.append('file', blob, 'recording.webm');
            formData.append('history', JSON.stringify(conversation));

            try {{
                const response = await fetch('/sendToGnome', {{
                    method: 'POST',
                    body: formData
                }});
                const data = await response.json();
                console.log(data);
                console.log(data['messages']);
                if (data['messages']) {{
                    addMessage(data['messages'][0]['sent'],"user");
                    addMessage(data['messages'][1]['recieved'], "gnome");

                    const audioBytes = atob(data['audio'][2]['audio']);
                    const audioArray = new Uint8Array(audioBytes.length);
                    for (let i = 0; i < audioBytes.length; i++) {{
                        audioArray[i] = audioBytes.charCodeAt(i);
                    }}
                    const audioBlob = new Blob([audioArray], {{ type: "audio/wav" }});
                    const audioUrl = URL.createObjectURL(audioBlob);

                    // Play audio
                    const audio = new Audio(audioUrl);
                    audio.play();

                }}
            }} catch (err) {{
                addMessage("Error sending voice message", "gnome");
            }}

            // Restore input
            userInput.value = "";
            userInput.disabled = false;
            userInput.focus();
        }};

        recorder.start();
        setTimeout(() => recorder.stop(), 10000); // 10 sec recording
    }} catch (err) {{
        alert("Microphone access denied or error: " + err);
    }}
}});
</script>


"""


