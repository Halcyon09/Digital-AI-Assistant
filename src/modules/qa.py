import streamlit as st
import time
from modules import prompts
from modules.settings import cargar_api_gemini

model = cargar_api_gemini() # Inicializar modelo de IA Gemini

def inicializar_chat():
    """
    Inicializa las variables de estado necesarias para el chat.

    Parámetros:
    -----------
    Ninguno

    Retorna:
    --------
    Ninguno (modifica st.session_state)

    Proceso:
    --------
    1. Verifica si el chat ya está iniciado
    2. Inicializa el historial de conversación vacío
    3. Prepara el objeto de chat de Gemini
    """
    # Verificar si ya se inició el chat anteriormente
    if "chat_iniciado" not in st.session_state:
        st.session_state.chat_iniciado = False

    # Inicializar historial de mensajes vacío
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Inicializar objeto de chat de Gemini
    if "gemini_chat" not in st.session_state:
        st.session_state.gemini_chat = None

def preparar_contexto_inicial():
    """
    Prepara el contexto inicial del asistente de productividad.

    Parámetros:
    -----------
    Ninguno

    Retorna:
    --------
    str
        Contexto con instrucciones base para el modelo.

    Proceso:
    --------
    1. Define el rol del agente como coach digital de productividad.
    2. Establece el tono (empático, motivador y práctico).
    3. Proporciona las reglas de interacción iniciales.
    """
    contexto_inicial = """
    Eres un asistente inteligente especializado en productividad personal y gestión del tiempo.
    Tu objetivo es ayudar al usuario a planificar mejor sus tareas, organizar sus metas y mejorar
    sus hábitos de estudio o trabajo.

    Reglas principales:
    - Ofrece respuestas breves, claras y útiles.
    - Usa un tono motivador y empático.
    - Si el usuario no proporciona suficiente contexto, pídele amablemente más detalles.
    - No inventes información personal, trabaja con lo que el usuario proporcione.

    Cuando saludes por primera vez, pregúntale al usuario cuáles son sus metas o tareas
    principales esta semana.
    """
    
    return contexto_inicial

def enviar_mensaje_inicial():
    """
    Envía el mensaje de bienvenida inicial al usuario y prepara el chat.

    Parámetros:
    -----------
    Ninguno

    Retorna:
    --------
    tuple
        - bool: True si fue exitoso, False si ocurrió un error.
        - str: Mensaje de bienvenida o error.
    """
    try:
        # Iniciar nueva sesión de chat con Gemini (historial vacío)
        st.session_state.gemini_chat = model.start_chat(history=[])

        # Obtener contexto inicial preparado
        contexto = preparar_contexto_inicial()

        # Crear mensaje inicial con contexto e instrucción de saludo
        mensaje_inicial = f"""
        {contexto}

        Ahora saluda al usuario y pregúntale qué aspecto de su productividad
        o planificación desea mejorar esta semana.
        """

        # Enviar mensaje inicial al modelo y obtener respuesta
        response = st.session_state.gemini_chat.send_message(mensaje_inicial)

        # Agregar saludo del asistente al historial de chat
        st.session_state.chat_history.append({
            "role": "assistant",           # Rol del mensaje (asistente)
            "content": response.text,      # Contenido de la respuesta
            "timestamp": time.time()       # Marca de tiempo del mensaje
        })

        st.session_state.chat_iniciado = True

        return True, response.text         # Retorno exitoso con saludo
    
    except Exception as e:
        # Capturar y retornar cualquier error de inicialización 
        return False, f"Error al inicializar el chat: {e}"
    
def procesar_mensaje_usuario(user_input, action="organize"):
    """
    Procesa el mensaje del usuario y genera la respuesta del asistente.

    Parámetros:
    -----------
    user_input : str
        Texto escrito por el usuario (tareas, metas, actividades, etc.)
    action : str
        Tipo de acción a realizar: "organize", "advise" o "summary"

    Retorna:
    --------
    tuple
        - bool: True si fue exitoso, False si hubo error.
        - str: Respuesta generada por la IA.
    """
    try:
        if action == "organize":
            prompt_text = prompts.prompt_organizar_tareas(user_input)
        elif action == "advise":
            prompt_text = prompts.prompt_consejos_productividad(user_input)
        elif action == "summary":
            prompt_text = prompts.prompt_resumen_semana(user_input)
        else:
            prompt_text = f"El usuario dice: {user_input}"

        response = st.session_state.gemini_chat.send_message(prompt_text)

        st.session_state.chat_history.extend([
            {
                "role": "user",
                "content": user_input,
                "timestamp": time.time(),
                "action": action
            },
            {
                "role": "assistant",
                "content": response.text,
                "timestamp": time.time(),
                "action": action
            }
        ])

        return True, response.text
    
    except Exception as e:
        return False, f"Error al enviar mensaje: {e}"
    
def mostrar_mensaje(mensaje, role):
    """
    Muestra un mensaje en la interfaz de chat con el formato adecuado.

    Parámetros:
    -----------
    mensaje : dict
        Diccionario con la clave 'content' (texto del mensaje)
    role : str
        Rol del mensaje ('user' o 'assistant')

    Retorna:
    --------
    Ninguno (se muestra en pantalla)
    """
    if role == "user":
        with st.chat_message("user"):
            st.write(mensaje["content"])
    else:
        with st.chat_message("assistant"):
            st.write(mensaje["content"])
