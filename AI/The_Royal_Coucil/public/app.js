const chat = document.getElementById("chat");
const input = document.getElementById("msg");
const sendBtn = document.getElementById("send");
const typing = document.getElementById("typing");

function addMessage(text, sender) {
  const msg = document.createElement("div");
  msg.className = `message ${sender}`;

  const label = document.createElement("div");
  label.className = "label";
  label.textContent = sender === "player" ? "You" : "Oracle";

  const body = document.createElement("div");
  body.textContent = text;

  msg.appendChild(label);
  msg.appendChild(body);
  chat.appendChild(msg);

  chat.scrollTop = chat.scrollHeight;
}

async function sendMessage() {
  const message = input.value.trim();
  if (!message) return;

  input.value = "";
  addMessage(message, "player");

  typing.classList.remove("hidden");

  try {
    const res = await fetch("/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message })
    });

    const data = await res.json();
    addMessage(data.reply, "oracle");
  } catch {
    addMessage("The council is silent.", "oracle");
  } finally {
    typing.classList.add("hidden");
  }
}

sendBtn.addEventListener("click", sendMessage);

input.addEventListener("keydown", (e) => {
  if (e.key === "Enter") sendMessage();
});
