def prompt_organizar_tareas(tareas_usuario):
    """
    Genera un prompt para que la IA organice y priorice las tareas del usuario.
    
    Parámetros:
    -----------
    tareas_usuario : str
        Texto libre ingresado por el usuario que describe tareas, pendientes o metas.
        
    Retorna:
    --------
    str
        Prompt estructurado que orienta al modelo a generar un plan organizado de tareas.

    Proceso:
    --------
    1. Recibe el texto del usuario con sus pendientes o metas.
    2. Solicita al modelo priorizar, estimar tiempos y crear un plan diario/semanal.
    3. Pide formato claro y cociso, con viñetas o pasos sugeridos.
    """
    prompt = f"""
        Eres un asistente de productividad personal experto en gestión del tiempo.
        El usuario te ha proporcionado la siguiente lista de tareas o metas:

        {tareas_usuario}

        Tu objetivo es:
        - Organizar estas tareas por prioridad (alta, media, baja).
        - Sugerir un orden lógico para completarlas.
        - Recomendar bloques de tiempo o distribución por días (si aplica).
        - Ser claro, motivador y práctico en tus recomendaciones.
        
        Devuelve la respuesta en formato estructurado (por ejemplo, usando bullet points).
        """
    return prompt

def prompt_consejos_productividad(contexto_usuario):
    """
    Genera un prompt para que la IA ofrezca consejos personalizados de productividad.
    
    Parámetros:
    -----------
    contexto_usuario : str
        Texto descriptivo del usuario sobre su estilo de trabajo o problemas comunes
        (pro ejemplo: "me cuesta concentrarme", "tengo muchas interrupciones", etc.)

    Retorna:
    --------
    str
        Prompt estructurado que orienta al modelo a generar consejos adaptados al contexto.

    Proceso:
    --------
    1. Recive el contexto general del usuario.
    2. Solicita al modelo ofrecer recomendaciones realistas y personalizadas.
    3. Limita la respuesta a entre 4 y 6 consejos prácticos.
    """
    prompt = f"""
    Actúa como un coach de productividad experimentado.
    El usuario describe su situación actual de la siguiente forma:

    "{contexto_usuario}"

    Basado en ello:
    - Ofrece entre 4 y 6 consejos prácticos para mejorar la organización y concentración.
    - Considera estrategias de gestión del tiempo (Pomodoro, Eisenhower, time blocking, etc.).
    - Evita respuestas genéricas: enfócate en recomendaciones útiles y accionables.
    - Mantén un tono empático y motivador.
    """
    return prompt

def prompt_resumen_semana(actividades_usuario):
    """
    Genera un prompt para que la IA cree un resumen de progreso semanal.

    Parámetros:
    -----------
    actividades_usuario : str
        Texto con una lista o descripción de actividades realizadas durante la semana.

    Retorna:
    --------
    str
        Prompt para que la IA genera un resumen de progreso, identificando logros y mejoras.

    Proceso:
    --------
    1. Recibe las actividades o tareas completadas del usuario.
    2. Solicita un análisis de productividad (qué se logró, qué se puede mejorar)
    3. Pide sugerencias breves para la siguiente semana.
    """
    prompt = f"""
    Eres un asistente que ayuda al usuario a reflexionar sobre su semana de trabajo o estudio.
    Estas fueron sus actividades y resultados recientes:

    {actividades_usuario}

    Tu tarea es:
    - Elaborar un breve resumen motivador de la semana.
    - Identificar logros, avances o buenas prácticas.
    - Mencionar uno o dos aspectos que el usuario podría mejorar.
    - Finalizar con una recomendación concreta para la próxima semana.

    Presenta la respuesta de manera breve y clara, con subtítulos o viñetas si es útil.
    """
    return prompt
