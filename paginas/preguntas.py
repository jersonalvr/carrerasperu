# paginas/preguntas.py

import streamlit as st
import pandas as pd
import plotly.express as px
import re
import requests
import json

def display():
    st.title("Chat de Preguntas y Respuestas")

    # Cargar la clave de RapidAPI desde los secretos de Streamlit
    rapidapi_key = st.secrets["RAPIDAPI"]["key"]

    # Inicializar el historial de chat en la sesión
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Función para generar la respuesta basada en la entrada del usuario
    def generar_respuesta_rapidapi(user_input, context):
        url = "https://cheapest-gpt-4-turbo-gpt-4-vision-chatgpt-openai-ai-api.p.rapidapi.com/v1/chat/completions"
        
        prompt = f"""
        Contexto:
        {context}
        
        Usuario: {user_input}
        Asistente:
        """

        payload = {
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "model": "gpt-4",
            "max_tokens": 1000,
            "temperature": 0.7
        }
        headers = {
            "x-rapidapi-key": rapidapi_key,
            "x-rapidapi-host": "cheapest-gpt-4-turbo-gpt-4-vision-chatgpt-openai-ai-api.p.rapidapi.com",
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()  # Raise an exception for bad status codes
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
        except requests.RequestException as e:
            st.error(f"Error al comunicarse con la API de RapidAPI: {e}")
            return ""
        except Exception as e:
            st.error(f"Error inesperado: {e}")
            return ""

    # Función para cargar y preparar los datos como contexto
    @st.cache_data
    def cargar_contexto():
        # URLs de los archivos Excel
        ingresos_universitaria_url = "https://cdn.www.gob.pe/uploads/document/file/5901478/5207826-universitarias_mp_nacional.xlsx"
        demanda_universitaria_url = "https://cdn.www.gob.pe/uploads/document/file/5988129/5306104-md_universitarias_nacional.xlsx"
        ingresos_tecnica_url = "https://cdn.www.gob.pe/uploads/document/file/5901305/5207826-tecnicas_mp_nacional.xlsx"
        demanda_tecnica_url = "https://cdn.www.gob.pe/uploads/document/file/5988189/5306104-md_tecnicas_nacional.xlsx"

        # Cargar datos universitarias
        ingresos_uni_df = pd.read_excel(ingresos_universitaria_url, usecols="C:E", skiprows=4, nrows=68)
        ingresos_uni_df.columns = ['Carrera', 'Ingreso_promedio', 'Minimo_Maximo']

        ingresos_uni_df['Ingreso_promedio'] = ingresos_uni_df['Ingreso_promedio'].astype(str).str.replace(r'[^\d]', '', regex=True).astype(int)

        def extract_min_max(s):
            numbers = re.findall(r'\d{1,3}(?:\s\d{3})*', s)
            if len(numbers) >= 2:
                min_val = int(numbers[0].replace(' ', ''))
                max_val = int(numbers[1].replace(' ', ''))
                return pd.Series([min_val, max_val])
            else:
                return pd.Series([None, None])

        ingresos_uni_df[['Ingreso_Minimo', 'Ingreso_Maximo']] = ingresos_uni_df['Minimo_Maximo'].apply(extract_min_max)
        ingresos_uni_df.drop('Minimo_Maximo', axis=1, inplace=True)

        demanda_uni_df = pd.read_excel(demanda_universitaria_url, usecols="C:D", skiprows=4, nrows=60)
        demanda_uni_df.columns = ['Carrera', 'Puestos_solicitados_2024']
        demanda_uni_df['Puestos_solicitados_2024'] = demanda_uni_df['Puestos_solicitados_2024'].astype(str).str.replace(r'[^\d]', '', regex=True).astype(int)

        # Cargar datos técnicas
        ingresos_tecnica_df = pd.read_excel(ingresos_tecnica_url, usecols="C:E", skiprows=4, nrows=31)
        ingresos_tecnica_df.columns = ['Carrera', 'Ingreso_promedio', 'Minimo_Maximo']
        ingresos_tecnica_df['Ingreso_promedio'] = ingresos_tecnica_df['Ingreso_promedio'].astype(str).str.replace(r'[^\d]', '', regex=True).astype(int)
        ingresos_tecnica_df[['Ingreso_Minimo', 'Ingreso_Maximo']] = ingresos_tecnica_df['Minimo_Maximo'].apply(extract_min_max)
        ingresos_tecnica_df.drop('Minimo_Maximo', axis=1, inplace=True)

        demanda_tecnica_df = pd.read_excel(demanda_tecnica_url, usecols="C:D", skiprows=4, nrows=39)
        demanda_tecnica_df.columns = ['Carrera', 'Puestos_solicitados_2024']
        demanda_tecnica_df['Puestos_solicitados_2024'] = demanda_tecnica_df['Puestos_solicitados_2024'].astype(str).str.replace(r'[^\d]', '', regex=True).astype(int)

        # Unir datasets universitarias
        merged_uni_df = pd.merge(ingresos_uni_df, demanda_uni_df, on='Carrera', how='inner')

        # Unir datasets técnicas
        merged_tecnica_df = pd.merge(ingresos_tecnica_df, demanda_tecnica_df, on='Carrera', how='inner')

        # Combinar ambos
        combined_df = pd.concat([merged_uni_df, merged_tecnica_df], ignore_index=True)

        # Seleccionar columnas relevantes
        combined_df = combined_df[['Carrera', 'Ingreso_promedio', 'Ingreso_Minimo', 'Ingreso_Maximo', 'Puestos_solicitados_2024']]

        # Crear un resumen para el contexto
        contexto = "Datos de Carreras en Perú:\n\n"

        # Ingresos
        contexto += "Ingresos Promedios por Carrera:\n"
        for index, row in combined_df.iterrows():
            contexto += f"- {row['Carrera']}: S/ {row['Ingreso_promedio']} (Mínimo: S/ {row['Ingreso_Minimo']}, Máximo: S/ {row['Ingreso_Maximo']})\n"

        # Puestos Solicitados
        contexto += "\nPuestos Solicitados en 2024 por Carrera:\n"
        for index, row in combined_df.iterrows():
            contexto += f"- {row['Carrera']}: {row['Puestos_solicitados_2024']} puestos\n"

        return contexto

    # Cargar el contexto
    contexto = cargar_contexto()

    # Interfaz de chat
    st.markdown("### Chat")

    user_input = st.text_input("Haz una pregunta sobre los datos de carreras:", "")

    if st.button("Enviar") and user_input:
        # Añadir el mensaje del usuario al historial
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        # Generar la respuesta utilizando la API de RapidAPI GPT-4
        respuesta = generar_respuesta_rapidapi(user_input, contexto)

        if respuesta:
            # Añadir la respuesta al historial
            st.session_state.chat_history.append({"role": "assistant", "content": respuesta})

    # Mostrar el historial del chat
    for chat in st.session_state.chat_history:
        if chat["role"] == "user":
            st.markdown(f"**Tú:** {chat['content']}")
        else:
            st.markdown(f"**Asistente:** {chat['content']}")

    # Sugerencias de preguntas
    st.markdown("### Sugerencias de Preguntas")
    sugerencias = [
        "¿Cuál es la carrera universitaria con mayor ingreso promedio?",
        "¿Cuántos puestos se solicitaron para Ingeniería de Transportes en 2024?",
        "¿Cuál es el ingreso máximo de Administración de Recursos Humanos?",
        "¿Qué carrera técnica tiene el ingreso mínimo más alto?",
        "¿Cuáles son las top 5 carreras con más puestos solicitados en 2024?"
    ]

    for sugerencia in sugerencias:
        if st.button(sugerencia):
            # Simular la entrada del usuario
            st.session_state.chat_history.append({"role": "user", "content": sugerencia})
            respuesta = generar_respuesta_rapidapi(sugerencia, contexto)
            if respuesta:
                st.session_state.chat_history.append({"role": "assistant", "content": respuesta})

    # Pie de página con información adicional
    footnote = """
    <div style="text-align: left; font-size: 10px; margin-top: 50px;">
        <strong>PERÚ:</strong> REMUNERACIÓN PROMEDIO MENSUAL EN EL SECTOR FORMAL PRIVADO, MÍNIMA Y MÁXIMA DE JÓVENES 
        PROFESIONALES UNIVERSITARIOS Y TÉCNICOS, SEGÚN FAMILIA DE CARRERAS, NOVIEMBRE 2022 - OCTUBRE 2023. (Soles)<br>
        <strong>Notas:</strong><br>
        - Comprende información de trabajadores jóvenes de 18 a 29 años egresados independientemente de su año de egreso.<br>
        - Las remuneraciones son calculadas considerando a los trabajadores con empleo dependiente del sector privado formal en el Perú, cuyas remuneraciones son iguales o mayores a la Remuneración Mínima Vital vigente.<br>
        - Se excluyen las familias de carreras con menos de 25 casos.<br>
        (1) Las denominaciones de familias de carreras corresponden a la agrupación a 3 dígitos (Campo Detallado) del “Clasificador de Carreras de Educación Superior y Técnico Productivas, 2014” del INEI.<br>
        (2) Los mínimos y máximos corresponden a los percentiles 10 y 90 del promedio de los ingresos, redondeados a las centenas.<br>
        (3) Otras Carreras de Administración comprende las siguientes carreras a 6 dígitos: Administración de Recursos Humanos, Administración de Servicios de Postales, Administrativo, Agencia de Desarrollo Integral, Planificación Empresarial, Planificación y Gestión de Desarrollo, y Supervisión de Operaciones.<br>
        (4) Otras Carreras de Educación comprende la siguiente carrera a 6 dígitos: Educación (Incluye Educación Básica Alternativa).<br>
        Fuente: MTPE - Planilla Electrónica (T-Registro y PLAME), noviembre 2022 a octubre 2023.<br>
        Elaboración: MTPE- DGPE - Dirección de Investigación Socio Económico Laboral (DISEL).<br><br>
        <strong>PERÚ:</strong> PERSONAL QUE LAS EMPRESAS CONTRATARÍAN PARA OCUPAR NUEVOS PUESTOS DE TRABAJO DE NATURALEZA PERMANENTE PARA PROFESIONALES UNIVERSITARIOS Y TÉCNICOS, SEGÚN CARRERAS, 2024<br>
        Nota: Para cada puesto de trabajo solicitado se puede presentar más de una carrera.<br>
        Fuente: MTPE - Encuesta de Demanda Ocupacional, 2023.<br>
        Elaboración: MTPE - DGPE - Dirección de Investigación Socio Económico Laboral (DISEL).
    </div>
    """
    st.markdown(footnote, unsafe_allow_html=True)
