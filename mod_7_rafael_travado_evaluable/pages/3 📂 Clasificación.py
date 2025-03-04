import os
import time
import gdown
import joblib
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import plotly.express as px

# =================== Cargar el Dataset desde session_state ===================
if "diamond_data" in st.session_state:
    df = st.session_state.diamond_data
else:
    st.error("⚠️ Error: No se ha encontrado el dataset. Regresa a la página de inicio.")
    st.stop()

# =================== URL del modelo en Google Drive ===================
modelo_path = "model_classification.joblib"  # Ruta simple sin carpeta
modelo_drive_url = "https://drive.google.com/uc?id=1O7E7Q4u3bn4AuVn5tkIizLhgtDnqTBew"

# =================== Cargar el Modelo de Clasificación ===================
if os.path.exists(modelo_path):
    try:
        with st.spinner("Cargando el modelo de clasificación desde local..."):
            modelo_clasificacion = joblib.load(modelo_path)
        st.success("✅ Modelo cargado correctamente desde local")
    except Exception as e:
        st.error(f"❌ Error al cargar el modelo local: {e}")
        st.stop()
else:
    st.warning("⚠️ No se encontró el modelo local. Intentando descargar desde Google Drive...")

    try:
        with st.spinner("Descargando modelo de clasificación desde Google Drive..."):
            gdown.download(modelo_drive_url, modelo_path, quiet=False)

        with st.spinner("Cargando el modelo descargado..."):
            modelo_clasificacion = joblib.load(modelo_path)

        st.success("✅ Modelo descargado y cargado correctamente desde Google Drive")
    except Exception as e:
        st.error(f"❌ Error al descargar el modelo: {e}. No se puede continuar sin el modelo.")
        st.stop()
    
# =================== Información del Dataset ===================
with st.sidebar.expander("📂 **Información del Dataset**", expanded=True):
    st.markdown(f"""
    <div style="font-size: 14px;">
    - 🔹 <b>Registros:</b> {df.shape[0]:,}  
    - 🔸 <b>Variables:</b> {df.shape[1]}  
    - 📊 <b>Memoria:</b> {df.memory_usage(deep=True).sum() / (1024*1024):.2f} MB  
    </div>
    """, unsafe_allow_html=True)

st.sidebar.markdown("<hr style='border:1px solid #ddd;'>", unsafe_allow_html=True)

# =================== Información del Autor ===================
st.sidebar.markdown("""
<div style="text-align: center;">
    <h3 style="color: #333;">👨‍💻 <b>Autor del Proyecto</b></h3>
    <p style="font-size: 16px; font-weight: bold; margin-bottom: 5px;">Rafael Travado Fernández</p>
    <p style="font-size: 14px; font-style: italic; color: #666;">📚 Bootcamp Data Science 2025</p>
</div>
""", unsafe_allow_html=True)

# =================== Enlaces a Redes Sociales ===================
st.sidebar.markdown("""
<div style="text-align: center;">
    <a href="https://github.com/Rafael-TF" target="_blank">
        <img src="https://img.shields.io/badge/GitHub-000?style=for-the-badge&logo=github&logoColor=white" width="110">
    </a>  
    <a href="https://www.linkedin.com/in/rafael-travado-4a1b6437/" target="_blank">
        <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" width="110">
    </a>  
    <a href="https://rafaeltravado.netlify.app/" target="_blank">
        <img src="https://img.shields.io/badge/Portfolio-3A86FF?style=for-the-badge&logo=google-chrome&logoColor=white" width="110">
    </a>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("<hr style='border:1px solid #ddd;'>", unsafe_allow_html=True)

# =================== Información Adicional ===================
st.sidebar.markdown("""
**📝 Última actualización:** Marzo 2025  
**📊 Desarrollado con:** Python, Streamlit, Seaborn, Plotly  
**💡 Objetivo:** Predicción de precios y clasificación de diamantes  
""", unsafe_allow_html=True)

# =================== Página de Clasificación ===================
st.title("⚡ Predicción del Corte del Diamante")

st.markdown("""
💎 **Descubre la calidad del corte de un diamante en función de sus características.**  
🔍 *Introduce los atributos del diamante y nuestro modelo te dirá su calidad esperada.*  
""")

# =================== Formulario de Predicción ===================
st.markdown("### 🎯 Simulador de Clasificación del Corte")

with st.form("classification_form"):
    st.markdown("<h4 style='color:#FF6B6B;'>📌 Características del Diamante</h4>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        carat = st.slider("💎 Quilates", min_value=0.2, max_value=5.0, value=1.0, step=0.1)
        depth = st.slider("📏 Profundidad (%)", min_value=40.0, max_value=80.0, value=61.5, step=0.1)
        table = st.slider("📐 Tabla (%)", min_value=40.0, max_value=80.0, value=57.0, step=0.1)
        x = st.slider("📏 Longitud (x)", min_value=0.0, max_value=10.0, value=5.5, step=0.1)
        y = st.slider("📏 Ancho (y)", min_value=0.0, max_value=10.0, value=5.5, step=0.1)
        z = st.slider("📏 Altura (z)", min_value=0.0, max_value=10.0, value=3.5, step=0.1)
        price = st.number_input("💰 Precio del Diamante ($)", min_value=100, max_value=20000, value=5000, step=50)
    
    with col2:
        color = st.selectbox("🎨 Color", df['color'].unique())
        clarity = st.selectbox("🔍 Claridad", df['clarity'].unique())
    
    st.markdown("---")
    classify_button = st.form_submit_button("⚡ Clasificar Corte")
    
if classify_button:
    try:
        # =================== Transformar Datos para la Clasificación ===================
        input_data = pd.DataFrame({
            'carat': [carat],
            'depth': [depth],
            'table': [table],
            'x': [x],
            'y': [y],
            'z': [z],
            'price': [price],
            'color': [color],
            'clarity': [clarity]
        })

        # Transformar los datos según el preprocesador del modelo
        column_transformer = modelo_clasificacion.named_steps['columntransformer']
        input_data_transformed = column_transformer.transform(input_data)

        # Realizar la predicción
        with st.spinner("🧐 Clasificando el corte del diamante..."):
            time.sleep(1)
            corte_predicho = modelo_clasificacion.named_steps['randomforestclassifier'].predict(input_data_transformed)[0]
            proba_predicho = modelo_clasificacion.named_steps['randomforestclassifier'].predict_proba(input_data_transformed)

        # =================== Mostrar Resultados ===================
        st.markdown("<h3 style='color:#FF6B6B;'>📊 Resultado de la Clasificación</h3>", unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="background-color: #ffe6e6; padding: 30px; border-radius: 15px; border-left: 8px solid #FF6B6B; 
        text-align: center; box-shadow: 0px 4px 12px rgba(0,0,0,0.1);">
            <h2 style="color: #FF6B6B; margin-top: 0; font-size: 36px;">🔍 Corte Predicho: {corte_predicho}</h2>
        </div>
        """, unsafe_allow_html=True)

        # =================== Visualización de Probabilidades ===================
        st.markdown("### 🔬 Probabilidades de Clasificación")
        df_proba = pd.DataFrame(proba_predicho, columns=modelo_clasificacion.named_steps['randomforestclassifier'].classes_)
        st.bar_chart(df_proba.T)

        # =================== Explicación de Factores ===================
        st.markdown("### 🧠 Factores Claves en la Predicción")
        st.markdown(f"""
        - **Quilates (Carat):** El tamaño del diamante influye en su clasificación.
        - **Precio:** Diamantes más caros suelen tener cortes de mayor calidad.
        - **Color y Claridad:** Factores estéticos que pueden impactar la clasificación.
        - **Proporciones (Profundidad, Tabla, Dimensiones):** Determinan cómo refleja la luz el diamante.
        """)

    except Exception as e:
        st.error(f"❌ Error al realizar la clasificación: {e}")

# =================== Footer ===================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #555; font-size: 14px;'>
     Desarrollado para el Bootcamp Data Science 2025  
    <p style='color: #777; font-size: 12px;'>Última actualización: Marzo 2025</p>
</div>
""", unsafe_allow_html=True)