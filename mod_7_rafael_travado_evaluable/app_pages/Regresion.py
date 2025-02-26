import time
import joblib
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns

df = sns.load_dataset("diamonds")

# Convertir columnas categóricas a tipo string para evitar errores
categorical_cols = ['cut', 'color', 'clarity']
df[categorical_cols] = df[categorical_cols].astype(str)

# Cargar modelo entrenado
try:
    with st.spinner("Cargando el modelo de predicción..."):
        modelo = joblib.load("models/model_regression.joblib")
    st.success("✅ Modelo cargado correctamente")
except Exception as e:
    st.error(f"❌ Error al cargar el modelo: {e}")
    st.stop()

# =================== Página de Regresión ===================
st.title("📈 Predicción Avanzada del Precio de Diamantes")

# Banner estilizado con animación y sombras
st.markdown("""
<div style="background: linear-gradient(to right, #3A86FF, #6fb1fc); padding: 30px; border-radius: 15px; margin-bottom: 20px; text-align: center; box-shadow: 0px 5px 15px rgba(0,0,0,0.2); animation: fadeIn 1.2s ease-in-out;">
    <h1 style="color: white; margin: 0; font-size: 36px; font-weight: bold;">💎 Estimación Inteligente del Precio de Diamantes</h1>
    <p style="color: #ffffffb3; font-size: 18px; margin-top: 10px;">Un análisis basado en Machine Learning para predecir con precisión el precio de un diamante</p>
</div>
<style>
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
🔍 **Nuestro modelo de IA analiza múltiples factores del diamante y te ofrece la mejor estimación de precio.**

💡 *Introduce los parámetros de tu diamante y descubre su valor de mercado.*
""")

# Sección de predicción con diseño premium
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
        
        # =================== Comparaciones con Datos Reales ===================
        avg_price = df["price"].mean()
        avg_price_per_carat = df.groupby("carat")["price"].mean()
        avg_price_per_cut = df.groupby("cut")["price"].mean()
        
        if cut in avg_price_per_cut.index:
            price_for_closest_cut = avg_price_per_cut.loc[cut]
        else:
            price_for_closest_cut = avg_price
        
        closest_carat = avg_price_per_carat.index[np.abs(avg_price_per_carat.index - carat).argmin()]
        price_for_closest_carat = avg_price_per_carat.loc[closest_carat]
        
        # =================== Mostrar Resultados ===================
        st.markdown("<h3 style='color:#3A86FF;'>📊 Resultados de la Predicción</h3>", unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="background-color: #eaf4ff; padding: 30px; border-radius: 15px; border-left: 8px solid #3A86FF; text-align: center; box-shadow: 0px 4px 12px rgba(0,0,0,0.1);">
            <h2 style="color: #3A86FF; margin-top: 0; font-size: 36px;">💰 Precio Estimado: ${precio_predicho:,.2f}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("📈 Precio Promedio", f"${avg_price:,.2f}")
        
        with col2:
            st.metric(f"📊 Precio Medio para {closest_carat} Quilates", f"${price_for_closest_carat:,.2f}")
        
        with col3:
            st.metric(f"🔍 Precio Medio para {cut} Cut", f"${price_for_closest_cut:,.2f}")
    
    except Exception as e:
        st.error(f"❌ Error al realizar la predicción: {e}")