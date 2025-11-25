const API_CHAT = "http://127.0.0.1:8000/chat";
const API_UPLOAD = "http://127.0.0.1:8000/upload";

const chatContainer = document.getElementById("chat-container");
const input = document.getElementById("message-input");
const typingText = document.getElementById("typing");

const fileInput = document.getElementById("file-input");
const fileBtn = document.getElementById("file-btn");
const sendBtn = document.getElementById("send-btn");

/* Mostrar mensajes en pantalla */
function addMessage(text, sender) {
    const div = document.createElement("div");
    div.classList.add("message", sender);
    div.textContent = text;
    chatContainer.appendChild(div);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

/* ENVIAR MENSAJE DE TEXTO */
async function sendMessage() {
    const text = input.value.trim();
    if (!text) return;
    
    addMessage(text, "user");
    input.value = "";
    
    typingText.style.display = "block";
    
    try {
        const response = await fetch(API_CHAT, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                messages: [
                    { role: "user", content: text }
                ]
            })
        });
        
        const data = await response.json();
        typingText.style.display = "none";
        
        addMessage(data.reply, "bot");
    
    } catch (error) {
        typingText.style.display = "none";
        addMessage("⚠ Error al conectar con el servidor.", "bot");
    }
}

sendBtn.addEventListener("click", sendMessage);
input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") sendMessage();
});

/* SUBIR ARCHIVOS */
fileBtn.addEventListener("click", () => {
    fileInput.click();
});

fileInput.addEventListener("change", async () => {
    const file = fileInput.files[0];
    if (!file) return;
    
    addMessage("📎 Archivo enviado: " + file.name, "user");
    
    const formData = new FormData();
    formData.append("file", file);
    
    typingText.style.display = "block";
    
    try {
        const response = await fetch(API_UPLOAD, {
            method: "POST",
            body: formData,
        });
        
        const data = await response.json();
        typingText.style.display = "none";
        
        addMessage(data.reply, "bot");
    
    } catch (error) {
        typingText.style.display = "none";
        addMessage("⚠ Error al procesar archivo.", "bot");
    }
    
    fileInput.value = "";
});