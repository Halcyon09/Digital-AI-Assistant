import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI

# Cargar variables de entorno
load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
PORT = int(os.getenv("PORT", 8000))

if not API_KEY:
    raise Exception("Debes definir OPENAI_API_KEY en el archivo .env")

# Cliente OpenAI
client = OpenAI(api_key=API_KEY)

# FastAPI
app = FastAPI(title="API ChatGPT - Proyecto Universitario")

# CORS (para HTML)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # solo desarrollo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos
class ChatRequest(BaseModel):
    messages: list[dict]  # [{"role":"user","content":"hola"}]

class ChatResponse(BaseModel):
    reply: str

# -------------------------
# ENDPOINT CHAT
# -------------------------
@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=req.messages,
            temperature=0.7
        )

        return ChatResponse(
            reply=response.choices[0].message.content
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))