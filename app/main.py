import os
from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai

# Cargar variables de entorno
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp")

if not API_KEY:
    raise Exception("Debes definir GEMINI_API_KEY en tu archivo .env")

# Configurar API de Gemini
genai.configure(api_key=API_KEY)

# Inicializar modelo
try:
    model = genai.GenerativeModel(MODEL_NAME)
except Exception:
    raise Exception(
        f"Modelo '{MODEL_NAME}' no existe. Usa: gemini-2.0-flash-exp, gemini-1.5-pro."
    )

# FastAPI
app = FastAPI(title="API IA - Gemini Versión Estable")

# CORS para permitir que el HTML se conecte
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de petición
class ChatRequest(BaseModel):
    messages: list[dict]

# Modelo de respuesta
class ChatResponse(BaseModel):
    reply: str

# -----------------------------
# CHAT BÁSICO
# -----------------------------
@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    try:
        
        conversation = ""

        for msg in req.messages:
            role = msg.get("role", "user").upper()
            content = msg.get("content", "")
            conversation += f"{role}: {content}\n"

        response = model.generate_content(conversation)

        if not hasattr(response, "text"):
            raise Exception("La API de Gemini no devolvió texto.")

        return ChatResponse(reply=response.text)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -----------------------------
# SUBIR ARCHIVOS
# -----------------------------
@app.post("/upload", response_model=ChatResponse)
async def upload_file(
    file: UploadFile = File(...),
    message: str | None = None):
    try:
        # 1) Guardar archivo temporal
        temp_path = f"temp_{file.filename}"

        with open(temp_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # 2) Subir archivo a Gemini
        uploaded = genai.upload_file(temp_path)

        prompt = message if message else "Analiza este archivo y proporciona un resumen detallado del contenido."

        # 3) Generar respuesta del modelo
        response = model.generate_content([
            prompt,
            uploaded
        ])

        # 4) Eliminar archivo temporal
        os.remove(temp_path)

        # 5) Validar respuesta
        if not hasattr(response, "text"):
            raise Exception("La API de Gemini no devolvió texto.")

        return ChatResponse(reply=response.text)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar archivo: {str(e)}")
