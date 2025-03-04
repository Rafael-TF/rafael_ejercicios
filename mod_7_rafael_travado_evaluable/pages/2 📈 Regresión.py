import os
import time
import gdown
import joblib
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# =================== Cargar el Dataset desde session_state ===================
if "diamond_data" in st.session_state:
    df = st.session_state.diamond_data
else:
    st.error("⚠️ Error: No se ha encontrado el dataset. Regresa a la página de inicio.")
    st.stop()

# =================== URL del modelo en Google Drive ===================
modelo_drive_url = "https://drive.google.com/uc?id=1_BXt5mN391zac33WmvliAOKD7KalBzRe"
modelo_path = "model_regression.joblib"  # Ruta simple sin carpeta

# =================== Cargar el Modelo de Regresión ===================
if os.path.exists(modelo_path):
    try:
        with st.spinner("Cargando el modelo de regresión..."):
            modelo = joblib.load(modelo_path)
        st.success("✅ Modelo cargado correctamente")
    except Exception as e:
        st.error(f"❌ Error al cargar el modelo: {e}")
        st.stop()
else:
    st.warning("⚠️ No se encontró el modelo local. Descargando desde Google Drive...")

    try:
        with st.spinner("Descargando modelo de regresión desde Google Drive..."):
            gdown.download(modelo_drive_url, modelo_path, quiet=False)

        # Cargar el modelo directamente desde la memoria
        with st.spinner("Cargando el modelo descargado..."):
            modelo = joblib.load(modelo_path)

        st.success("✅ Modelo descargado y cargado correctamente desde Google Drive")
    except Exception as e:
        st.error(f"❌ Error al descargar el modelo: {e}")
        st.stop()

# =================== Sidebar con Información ===================
with st.sidebar.expander("📂 **Información del Dataset**", expanded=True):
    st.markdown(f"""
    - 🔹 **Registros:** {df.shape[0]:,}
    - 🔸 **Variables:** {df.shape[1]}
    - 📊 **Memoria:** {df.memory_usage(deep=True).sum() / (1024*1024):.2f} MB
    """)
    
st.sidebar.markdown("---")

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

# =================== Página de Regresión ===================
st.title("📈 Predicción del Precio de Diamantes")

st.markdown("""
💎 **Nuestro modelo de Machine Learning predice el precio de un diamante basándose en sus características físicas.**  
📊 *Selecciona los valores y descubre su precio estimado con precisión.*
""")

# =================== Formulario de Predicción ===================
st.markdown("### 🎯 Simulador de Predicción de Precios")

with st.form("prediction_form"):
    st.markdown("<h4 style='color:#3A86FF;'>📌 Configuración del Diamante</h4>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        carat = st.slider("💎 Quilates", min_value=0.2, max_value=5.0, value=1.0, step=0.1)
        depth = st.slider("📏 Profundidad (%)", min_value=40.0, max_value=80.0, value=61.5, step=0.1)
        table = st.slider("📐 Tabla (%)", min_value=40.0, max_value=80.0, value=57.0, step=0.1)
        x = st.slider("📏 Longitud (x)", min_value=0.0, max_value=10.0, value=5.5, step=0.1)
        y = st.slider("📏 Ancho (y)", min_value=0.0, max_value=10.0, value=5.5, step=0.1)
        z = st.slider("📏 Altura (z)", min_value=0.0, max_value=10.0, value=3.5, step=0.1)
    
    with col2:
        cut = st.selectbox("✨ Corte", df['cut'].unique())
        color = st.selectbox("🎨 Color", df['color'].unique())
        clarity = st.selectbox("🔍 Claridad", df['clarity'].unique())
    
    st.markdown("---")
    predict_button = st.form_submit_button("🚀 Predecir Precio")
    
if predict_button:
    try:
        input_data = pd.DataFrame({
            'carat': [carat],
            'depth': [depth],
            'table': [table],
            'x': [x],
            'y': [y],
            'z': [z],
            'cut': [cut],
            'color': [color],
            'clarity': [clarity]
        })
        
        with st.spinner("🧐 Calculando precio..."):
            time.sleep(1)
            precio_predicho = modelo.predict(input_data)[0]

        # =================== Visualización del Resultado ===================
        st.markdown("<h3 style='color:#3A86FF;'>📊 Resultado de la Predicción</h3>", unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="background-color: #eaf4ff; padding: 30px; border-radius: 15px; border-left: 8px solid #3A86FF; text-align: center;">
            <h2 style="color: #3A86FF;">💰 Precio Estimado: ${precio_predicho:,.2f}</h2>
        </div>
        """, unsafe_allow_html=True)

        # =================== Gráfico de Comparación ===================
        st.markdown("### 📊 Comparación con Datos Reales")
        avg_price = df.groupby("carat")["price"].mean().reset_index()
        
        fig = px.scatter(avg_price, x="carat", y="price", trendline="ols",
                         title="Precio Real Promedio vs. Precio Predicho",
                         labels={"carat": "Quilates", "price": "Precio ($)"})
        
        fig.add_scatter(x=[carat], y=[precio_predicho], mode='markers', 
                        marker=dict(color='red', size=12), 
                        name='Predicción')
        
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(f"❌ Error en la predicción: {e}")
        
    # =================== Footer ===================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #555; font-size: 14px;'>
     Desarrollado para el Bootcamp Data Science 2025   
    <p style='color: #777; font-size: 12px;'>Última actualización: Marzo 2025</p>
</div>
""", unsafe_allow_html=True)
