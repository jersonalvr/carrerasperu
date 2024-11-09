# modules/create_sidebar.py

import streamlit as st
from streamlit_option_menu import option_menu
from paginas import universitaria, tecnica, preguntas

def create_sidebar():
    # Añadir texto personalizado en el sidebar con markdown y HTML
    st.sidebar.markdown(
        f'''
        <div style="text-align: center; font-size: 18px; margin-bottom: 10px;">
            Análisis de Ingresos y Puestos Solicitados por Carrera
        </div>
        <div style="text-align: center; margin-bottom: 20px;">
            Elaborado por 
            <a href="https://www.linkedin.com/in/jersonalvr" target="_blank" style="text-decoration: none; color: inherit;">
                <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" alt="LinkedIn" width="20" style="vertical-align: middle; margin-right: 5px;"/>
                Jerson Ruiz Alva
            </a>
        </div>
        ''',
        unsafe_allow_html=True
    )

    # Crear el menú de opciones en el sidebar con option_menu
    with st.sidebar:
        selected = option_menu(
            menu_title="Menú",  # Título del menú
            options=["Universitaria", "Técnica", "Preguntas"],  # Opciones del menú
            icons=["mortarboard", "tools", "chat-left-dots-fill"],  # Íconos correspondientes
            menu_icon="cast",  # Ícono del menú principal
            default_index=0,  # Índice por defecto
            orientation="vertical"  # Orientación del menú
        )

    # Llama a la función de la página correspondiente en función de la selección
    if selected == "Universitaria":
        universitaria.display()
    elif selected == "Técnica":
        tecnica.display()
    elif selected == "Preguntas":
        preguntas.display()
