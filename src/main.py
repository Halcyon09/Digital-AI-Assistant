# --- existing code ---

import streamlit as st

st.set_page_config(
    page_title="Digital-AI-Assistant",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- Configuración inicial ---
st.title("Smart Productivity Assistant")
st.subheader("Asistente Inteligente de Productividad Personal")

# --- Configuración de API Key ---
st.markdown("### Configuración inicial")

# Verificar si ya existe la API Key en session state
if "gemini_api_key" not in st.session_state:
    st.session_state.gemini_api_key = ""

# Input para la API Key
api_key = st.text_input(
    "Ingresa tu API Key de Google Gemini:",
    value=st.session_state.gemini_api_key,
    type="password",
    help="Necesitas una API Key de Google Gemini para usar las funciones del asistente." \
    "Obtén tu clave en: https://aistudio.google.com/app/apikey"
)

# Guardar en session state cuando cambie
if api_key != st.session_state.gemini_api_key:
    st.session_state.gemini_api_key = api_key

# Mostrar estado de la configuración
if st.session_state.gemini_api_key:
    st.success("API Key configurada correctamente ✅")
else:
    st.warning("⚠️ Necesitas configurar tu API Key de Google Gemini para usar todas las funciones del asistente.")

st.divider()

st.markdown("""
### Tu Asistente Personal Impulsado por Inteligencia Artificial 🤖

**Smart Productivity Assistant** es un asistente digital diseñado para ayudarte a **gestionar tus tareas, metas y hábitos**
de forma más eficiente, utilizando modelos de **Inteligencia Artificial generativa** para analizar tus objetivos
y ofrecer recomendaciones personalizadas.
            
### 💼 ¿Qué puede hacer por ti?
            
- **Organización Inteligente**: Toma tu lista de tareas y las ordena por prioridad, fecha y esfuerzo estimado.
- **Recordatorios Automatizados**: Sugiere recordatorios inteligentes según tu carga de trabajo y metas.
- **Resumen Semanal**: Genera un análisis de tu progreso, destacando logros y áreas de mejora.
- **Asistente Conversacional**: Interactúa en lenguaje natural para recibir consejos y ajustes de planificación.
            
### 🧭 Flujo de trabajo simplificado:
            
1. **Tareas y Metas** → Registra tus objetivos o pendientes.
2. **Recomendaciones IA** → Obtén sugerencias automáticas para mejorar tu productividad.
3. **Resumen Semanal** → Revisa tus progresos y recibe retroalimentación personalizada.

⚙️ **Tecnologías**: Streamlit | scikit-learn | Google Gemini | Plotly | pandas
""")

# Información de navegación
if st.session_state.gemini_api_key:
    st.info("""
    **Usa la barra lateral** para navegar entre las diferentes secciones del asistente.
            
    💡 **Flujo recomendado**: sigue el orden de las páginas para obtener los mejores resultados:
    1. Ingreso de metas y tareas.
    2. Recomendaciones automáticas.
    3. Resumen y evaluación semanal.
    """)
else:
    st.info("""
    🔐 **Configura tu API Key arriba** para comenzar a utilizar el asistente.
            
    **Una vez configurada**, utiliza la barra lateral para navegar entre las secciones del agente.
    """)
