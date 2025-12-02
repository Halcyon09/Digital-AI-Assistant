const API_CHAT = "http://127.0.0.1:8000/chat";
const API_UPLOAD = "http://127.0.0.1:8000/upload";

const chatContainer = document.getElementById("chat-container");
const input = document.getElementById("message-input");
const typingText = document.getElementById("typing");

const fileInput = document.getElementById("file-input");
const fileBtn = document.getElementById("file-btn");
const sendBtn = document.getElementById("send-btn");

// Variable para almacenar el archivo seleccionado
let selectedFile = null;

/* Mostrar mensajes en pantalla */
function addMessage(text, sender) {
    const div = document.createElement("div");
    div.classList.add("message", sender);
    div.textContent = text;
    chatContainer.appendChild(div);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

/* ENVIAR MENSAJE DE TEXTO O ARCHIVO */
async function sendMessage() {
    const text = input.value.trim();
    
    
    if (selectedFile) {
        await sendFileWithMessage(text);
        return;
    }
    
    
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

/* ENVIAR ARCHIVO CON MENSAJE */
async function sendFileWithMessage(message) {
    if (!selectedFile) return;
    
    
    const userMessage = message 
        ? `📎 ${selectedFile.name}\n${message}` 
        : `📎 Archivo enviado: ${selectedFile.name}`;
    
    addMessage(userMessage, "user");
    input.value = "";
    
    const formData = new FormData();
    formData.append("file", selectedFile);
    
    
    if (message) {
        formData.append("message", message);
    }
    
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
    
    
    selectedFile = null;
    fileInput.value = "";
    updateFileButton();
}


function updateFileButton() {
    if (selectedFile) {
        fileBtn.textContent = "✓ " + selectedFile.name.substring(0, 15);
        fileBtn.style.backgroundColor = "#4CAF50";
        fileBtn.style.color = "white";
    } else {
        fileBtn.textContent = "📎";
        fileBtn.style.backgroundColor = "";
        fileBtn.style.color = "";
    }
}

sendBtn.addEventListener("click", sendMessage);
input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") sendMessage();
});

/* SELECCIONAR ARCHIVOS */
fileBtn.addEventListener("click", () => {
    fileInput.click();
});

fileInput.addEventListener("change", () => {
    const file = fileInput.files[0];
    if (file) {
        selectedFile = file;
        updateFileButton();
        
       
        input.focus();
        input.placeholder = `Escribe qué quieres hacer con ${file.name}...`;
    }
});