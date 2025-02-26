import time
import joblib
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import plotly.express as px
 
 # =================== Cargar Datos ===================
df = sns.load_dataset("diamonds")

# Convertir columnas categóricas a tipo string para evitar errores
categorical_cols = ['color', 'clarity']
df[categorical_cols] = df[categorical_cols].astype(str)

# Cargar modelo entrenado de clasificación
try:
    with st.spinner("Cargando el modelo de clasificación..."):
        modelo_clasificacion = joblib.load("model_classification.joblib")
    st.success("✅ Modelo cargado correctamente")
except Exception as e:
    st.error(f"❌ Error al cargar el modelo: {e}")
    st.stop()

# =================== Página de Clasificación ===================
st.title("⚡ Predicción del Corte del Diamante")

st.markdown("""
<div style="background: linear-gradient(to right, #FF6B6B, #FF8E8E); padding: 30px; border-radius: 15px; 
margin-bottom: 20px; text-align: center; box-shadow: 0px 5px 15px rgba(0,0,0,0.2); animation: fadeIn 1.2s ease-in-out;">
    <h1 style="color: white; margin: 0; font-size: 36px; font-weight: bold;">🔍 Clasificación de Calidad del Corte</h1>
    <p style="color: #ffffffb3; font-size: 18px; margin-top: 10px;">Un modelo de Machine Learning para predecir el tipo de corte de un diamante</p>
</div>
<style>
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
🔍 **Este modelo de clasificación predice la calidad del corte de un diamante en función de sus características.**

💡 *Introduce los atributos del diamante y obtén su clasificación.*
""")

# Sección de predicción con diseño premium
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
        # Crear DataFrame con los datos ingresados por el usuario
        input_data = pd.DataFrame({
            'carat': [carat],
            'depth': [depth],
            'table': [table],
            'x': [x],
            'y': [y],
            'z': [z],
            'price': [price],  # 🚀 Ahora agregamos el precio
            'color': [color],
            'clarity': [clarity]
        })

        # Asegurar que las columnas coinciden con las usadas en el entrenamiento
        expected_columns = modelo_clasificacion.feature_names_in_
        missing_cols = set(expected_columns) - set(input_data.columns)

        if missing_cols:
            st.error(f"❌ Error al realizar la clasificación: columnas faltantes: {missing_cols}")
        else:
            # Realizar la predicción
            with st.spinner("🧐 Clasificando el corte del diamante..."):
                time.sleep(1)
                corte_predicho = modelo_clasificacion.predict(input_data)[0]
                proba_predicho = modelo_clasificacion.predict_proba(input_data)

            # =================== Mostrar Resultados ===================
            st.markdown("<h3 style='color:#FF6B6B;'>📊 Resultado de la Clasificación</h3>", unsafe_allow_html=True)
            
            st.markdown(f"""
            <div style="background-color: #ffe6e6; padding: 30px; border-radius: 15px; border-left: 8px solid #FF6B6B; 
            text-align: center; box-shadow: 0px 4px 12px rgba(0,0,0,0.1);">
                <h2 style="color: #FF6B6B; margin-top: 0; font-size: 36px;">🔍 Corte Predicho: {corte_predicho}</h2>
            </div>
            """, unsafe_allow_html=True)

            # Mostrar probabilidades de predicción
            st.markdown("### 🔬 Probabilidades de Clasificación")
            df_proba = pd.DataFrame(proba_predicho, columns=modelo_clasificacion.classes_)
            st.bar_chart(df_proba.T)

            # Comparación con la base de datos
            st.markdown("### 📊 Distribución de Cortes en la Base de Datos")
            corte_counts = df['cut'].value_counts(normalize=True) * 100

            fig = px.bar(
                x=corte_counts.index,
                y=corte_counts.values,
                text=[f"{val:.2f}%" for val in corte_counts.values],
                labels={'x': 'Corte', 'y': 'Frecuencia (%)'},
                title="Distribución de Cortes en la Base de Datos",
                color=corte_counts.index,
                color_discrete_sequence=px.colors.qualitative.Set1
            )

            fig.update_traces(textposition='outside')
            fig.update_layout(height=400)

            st.plotly_chart(fig, use_container_width=True)

            # Mostrar interpretación de las variables
            st.markdown("### 🧠 Factores Claves en la Predicción")
            st.markdown(f"""
            - **Quilates (Carat)**: El tamaño del diamante influye en su clasificación.
            - **Precio**: Diamantes más caros suelen tener cortes de mayor calidad.
            - **Color y Claridad**: Factores estéticos que pueden impactar la clasificación.
            - **Proporciones (Profundidad, Tabla, Dimensiones)**: Determinan cómo refleja la luz el diamante.
            """)

    except Exception as e:
        st.error(f"❌ Error al realizar la clasificación: {e}")