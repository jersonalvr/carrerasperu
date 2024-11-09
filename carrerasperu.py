try:
    from modules.config_page import set_global_page_config
    set_global_page_config()

    from modules.create_sidebar import create_sidebar
    create_sidebar()
except ImportError as e:
    import streamlit as st
    st.error(f"Error de importación: {e}")
    st.error("Por favor, verifica que todas las dependencias estén instaladas correctamente.")
