# paginas/universitaria.py

import streamlit as st
import pandas as pd
import plotly.express as px
import re

def display():
    st.title("Análisis de Ingresos y Puestos Solicitados por Carrera Universitaria")
    
    # URLs de los archivos Excel
    ingresos_url = "https://cdn.www.gob.pe/uploads/document/file/5901478/5207826-universitarias_mp_nacional.xlsx"
    demanda_url = "https://cdn.www.gob.pe/uploads/document/file/5988129/5306104-md_universitarias_nacional.xlsx"
    
    @st.cache_data
    def load_ingresos_data(url):
        """
        Carga y procesa los datos de ingresos desde el archivo Excel.
        """
        # Cargar las columnas C, D, E; filas 5 a 72 (68 filas)
        df = pd.read_excel(url, usecols="C:E", skiprows=4, nrows=68)
        df.columns = ['Carrera', 'Ingreso_promedio', 'Minimo_Maximo']
        
        # Limpiar 'Ingreso_promedio': eliminar 'S/' y espacios, convertir a entero
        df['Ingreso_promedio'] = df['Ingreso_promedio'].astype(str).str.replace(r'[^\d]', '', regex=True).astype(int)
        
        # Función para extraer ingreso mínimo y máximo
        def extract_min_max(s):
            # Buscar números con posibles separadores de miles
            numbers = re.findall(r'\d{1,3}(?:\s\d{3})*', s)
            if len(numbers) >= 2:
                min_val = int(numbers[0].replace(' ', ''))
                max_val = int(numbers[1].replace(' ', ''))
                return pd.Series([min_val, max_val])
            else:
                return pd.Series([None, None])
        
        # Aplicar la función para extraer los valores
        df[['Ingreso_Minimo', 'Ingreso_Maximo']] = df['Minimo_Maximo'].apply(extract_min_max)
        df.drop('Minimo_Maximo', axis=1, inplace=True)
        
        return df

    @st.cache_data
    def load_demanda_data(url):
        """
        Carga y procesa los datos de demanda de puestos desde el archivo Excel.
        """
        # Cargar las columnas C y D; filas 5 a 64 (60 filas)
        df = pd.read_excel(url, usecols="C:D", skiprows=4, nrows=60)
        df.columns = ['Carrera', 'Puestos_solicitados_2024']
        
        # Limpiar 'Puestos_solicitados_2024': eliminar posibles caracteres no numéricos
        df['Puestos_solicitados_2024'] = df['Puestos_solicitados_2024'].astype(str).str.replace(r'[^\d]', '', regex=True).astype(int)
        
        return df

    # Cargar los datos
    ingresos_df = load_ingresos_data(ingresos_url)
    demanda_df = load_demanda_data(demanda_url)

    # Unir los datasets por 'Carrera'
    merged_df = pd.merge(ingresos_df, demanda_df, on='Carrera', how='inner')

    # Ordenar el dataframe por ingreso promedio descendente para el gráfico de ingresos
    ingresos_sorted_df = merged_df.sort_values(by='Ingreso_promedio', ascending=False)

    # Ordenar el dataframe por puestos solicitados ascendentes para el gráfico de puestos solicitados
    demanda_sorted_df = merged_df.sort_values(by='Puestos_solicitados_2024', ascending=True)

    # Mostrar el dataframe (opcional)
    with st.expander("Ver Datos Combinados"):
        st.dataframe(merged_df)

    # Gráfico 1: Ingreso Promedio por Carrera
    st.header("Ingreso Promedio por Carrera")
    fig1 = px.bar(
        ingresos_sorted_df,
        x='Ingreso_promedio',
        y='Carrera',
        orientation='h',
        title='Ingreso Promedio Mensual por Carrera',
        labels={'Ingreso_promedio': 'Ingreso Promedio (S/)', 'Carrera': 'Carrera'},
        hover_data={'Ingreso_promedio': ':.2f', 'Ingreso_Minimo': True, 'Ingreso_Maximo': True},
        template='plotly_white'
    )
    st.plotly_chart(fig1, use_container_width=True)

    # Gráfico 2: Puestos Solicitados por Carrera en 2024 (Ordenado de Menor a Mayor)
    st.header("Puestos Solicitados por Carrera en 2024")
    fig2 = px.bar(
        demanda_sorted_df,
        x='Puestos_solicitados_2024',
        y='Carrera',
        orientation='h',
        title='Puestos Solicitados en 2024 por Carrera',
        labels={'Puestos_solicitados_2024': 'Puestos Solicitados', 'Carrera': 'Carrera'},
        hover_data={'Puestos_solicitados_2024': True},
        template='plotly_white'
    )
    st.plotly_chart(fig2, use_container_width=True)

    # Gráfico 3: Relación entre Ingreso Promedio y Puestos Solicitados
    st.header("Relación entre Ingreso Promedio y Puestos Solicitados")
    fig3 = px.scatter(
        merged_df,
        x='Ingreso_promedio',
        y='Puestos_solicitados_2024',
        hover_name='Carrera',
        size='Puestos_solicitados_2024',
        title='Ingreso Promedio vs Puestos Solicitados',
        labels={'Ingreso_promedio': 'Ingreso Promedio (S/)', 'Puestos_solicitados_2024': 'Puestos Solicitados'},
        trendline='ols',
        template='plotly_white'
    )
    st.plotly_chart(fig3, use_container_width=True)

    # Gráfico 4: Top 10 Carreras con Más Puestos Solicitados
    st.header("Top 10 Carreras con Más Puestos Solicitados en 2024")
    top10_df = merged_df.nlargest(10, 'Puestos_solicitados_2024')
    fig4 = px.pie(
        top10_df,
        names='Carrera',
        values='Puestos_solicitados_2024',
        title='Distribución de Puestos Solicitados entre las Top 10 Carreras',
        hole=0.3,
        template='plotly_white'
    )
    st.plotly_chart(fig4, use_container_width=True)

    # Pie de página con información adicional
    footnote = """
    <div style="text-align: left; font-size: 10px; margin-top: 50px;">
        <strong>PERÚ:</strong> REMUNERACIÓN PROMEDIO MENSUAL EN EL SECTOR FORMAL PRIVADO, MÍNIMA Y MÁXIMA DE JÓVENES 
        PROFESIONALES UNIVERSITARIOS, SEGÚN FAMILIA DE CARRERAS, NOVIEMBRE 2022 - OCTUBRE 2023. (Soles)<br>
        <strong>Notas:</strong><br>
        - Comprende información de trabajadores jóvenes de 18 a 29 años egresados independientemente de su año de egreso.<br>
        - Las remuneraciones son calculadas considerando a los trabajadores con empleo dependiente del sector privado formal en el Perú, cuyas remuneraciones son iguales o mayores a la Remuneración Mínima Vital vigente.<br>
        - Se excluyen las familias de carreras con menos de 25 casos.<br>
        (1) Las denominaciones de familias de carreras corresponden a la agrupación a 3 dígitos (Campo Detallado) del “Clasificador de Carreras de Educación Superior y Técnico Productivas, 2014” del INEI.<br>
        (2) Los mínimos y máximos corresponden a los percentiles 10 y 90 del promedio de los ingresos, redondeados a las centenas.<br>
        (3) Otras Carreras de Administración comprende las siguientes carreras a 6 dígitos: Gestión y Alta Dirección; Relaciones Industriales; y Gestión de Recursos Humanos.<br>
        (4) Otras Ingenierías comprende las siguientes carreras a 6 dígitos: Ingeniería de Transportes e Ingeniería automotriz.<br>
        (5) Otras Carreras de Educación comprende la siguiente carrera a 6 dígitos: Educación (Incluye Ciencias de la Educación).<br>
        Fuente: MTPE - Planilla Electrónica (T-Registro y PLAME), noviembre 2022 a octubre 2023.<br>
        Elaboración: MTPE- DGPE - Dirección de Investigación Socio Económico Laboral (DISEL).<br><br>
        <strong>PERÚ:</strong> PERSONAL QUE LAS EMPRESAS CONTRATARÍAN PARA OCUPAR NUEVOS PUESTOS DE TRABAJO DE NATURALEZA PERMANENTE PARA PROFESIONALES UNIVERSITARIOS, SEGÚN CARRERAS, 2024<br>
        (1) Las denominaciones de familias de carreras corresponden a la agrupación a 3 dígitos (Campo Detallado) del “Clasificador de Carreras de Educación Superior y Técnico Productivas, 2014” del INEI.<br>
        (2) Otras Carreras de Administración comprende las siguientes carreras a 6 dígitos: Gestión y Alta Dirección; Relaciones Industriales; y Gestión de Recursos Humanos.<br>
        (3) Otras Ingenierías comprende las siguientes carreras a 6 dígitos: Ingeniería de Transportes e Ingeniería automotriz.<br>
        (4) Otras Carreras de Educación comprende la siguiente carrera a 6 dígitos: Educación (Incluye Ciencias de la Educación).<br>
        Nota: Para cada puestos de trabajo solicitado se puede presentar más de una carrera.<br>
        Fuente: MTPE - Encuesta de Demanda Ocupacional, 2023.<br>
        Elaboración: MTPE - DGPE - Dirección de Investigación Socio Económico Laboral (DISEL).
    </div>
    """
    st.markdown(footnote, unsafe_allow_html=True)
