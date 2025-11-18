import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

import google.generativeai as genai

# Cargar variables de entorno
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")  # Modelo actualizado

if not API_KEY:
    raise Exception("Debes definir GEMINI_API_KEY en tu archivo .env")

# Configurar API de Gemini
genai.configure(api_key=API_KEY)

# Validar modelo disponible
try:
    model = genai.GenerativeModel(MODEL_NAME)
except Exception:
    raise Exception(
        f"El modelo '{MODEL_NAME}' no existe o no es compatible. "
        f"Prueba con: gemini-2.0-flash, gemini-2.0-pro, gemini-1.5-flash."
    )

# FastAPI
app = FastAPI(title="API IA - Gemini Version Actualizada")

class ChatRequest(BaseModel):
    messages: list[dict]  # [{"role": "user", "content": "hola"}]

class ChatResponse(BaseModel):
    reply: str

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """
    Endpoint que envía mensajes a Gemini.
    Gemini NO usa 'messages' como OpenAI, así que convertimos todo a un prompt.
    """
    try:
        # Convertimos la conversación completa a un solo texto
        conversation_text = ""

        for msg in req.messages:
            role = msg.get("role", "user").upper()
            content = msg.get("content", "")
            conversation_text += f"{role}: {content}\n"

        # Enviar a Gemini
        response = model.generate_content(conversation_text)

        # Verificar si Gemini devolvió texto
        if not hasattr(response, "text"):
            raise Exception("La API de Gemini no devolvió texto válido.")

        return ChatResponse(reply=response.text)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))