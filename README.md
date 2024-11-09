# Análisis de Ingresos y Puestos Solicitados por Carrera

Este proyecto, construido en Python usando Streamlit, proporciona una interfaz visual para analizar datos de ingresos y demanda de puestos laborales en carreras universitarias y técnicas en el Perú. Permite a los usuarios explorar los ingresos promedio, mínimo y máximo, así como los puestos solicitados para el año 2024, segmentados por tipo de carrera.

## Estructura del Proyecto

- **modules/create_sidebar.py**: Define la barra lateral del proyecto, donde se incluye un menú de navegación para acceder a las diferentes secciones de análisis (Universitaria, Técnica y Preguntas).
- **paginas/universitaria.py**: Contiene la visualización y el análisis de datos relacionados con carreras universitarias.
- **paginas/tecnica.py**: Proporciona visualización y análisis de datos de carreras técnicas.
- **paginas/preguntas.py**: Implementa un chat interactivo de preguntas y respuestas sobre los datos disponibles, utilizando la API de RapidAPI y GPT-4 para generar respuestas en función del contexto de los datos.

## Archivos de Datos

Los datos utilizados en este proyecto son archivos Excel provenientes de fuentes públicas de Perú:
- Ingresos y demanda para carreras universitarias
- Ingresos y demanda para carreras técnicas

## Funcionalidades

1. **Análisis de Carreras Universitarias**: Visualización de los ingresos promedio, mínimo y máximo, así como de la demanda de puestos laborales para carreras universitarias.
2. **Análisis de Carreras Técnicas**: Similar al análisis universitario, pero enfocado en carreras técnicas.
3. **Chat Interactivo**: Un sistema de preguntas y respuestas donde los usuarios pueden hacer preguntas sobre los datos, y el sistema responde utilizando inteligencia artificial.

## Instalación y Configuración

1. **Requisitos**: 
   - Python 3.7+
   - Bibliotecas necesarias: Streamlit, Pandas, Plotly, Requests

2. **Instalación de Dependencias**:
   Ejecuta el siguiente comando para instalar las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. **API Key**:
   - Este proyecto utiliza la API de RapidAPI para el chat de preguntas y respuestas. Asegúrate de colocar tu clave en el archivo de configuración `secrets.toml` de Streamlit en la sección `RAPIDAPI`:
   ```toml
   [RAPIDAPI]
   key = "TU_API_KEY"
   ```

## Uso

Para iniciar la aplicación, ejecuta el siguiente comando:
```bash
streamlit run carrerasperu.py
```

### Navegación

- **Menú**: La barra lateral permite al usuario seleccionar entre las secciones Universitaria, Técnica y Preguntas.
- **Análisis Visual**: Cada sección de análisis presenta gráficos detallados sobre ingresos y demanda.
- **Chat de Preguntas**: Usa el chat para realizar consultas sobre los datos disponibles.

## Créditos

Creado por [Jerson Ruiz Alva](https://www.linkedin.com/in/jersonalvr).
