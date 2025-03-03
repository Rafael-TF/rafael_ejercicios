import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.graph_objects as go

# =================== Configuración de Página ===================
st.set_page_config(
    page_title="Diamond Analytics | Machine Learning",
    page_icon="\U0001F48E",
    layout="wide",
    initial_sidebar_state="collapsed"  # Oculta el sidebar
)

# =================== Cargar el Dataset en Session State ===================
if 'diamond_data' not in st.session_state:
    st.session_state.diamond_data = sns.load_dataset("diamonds")

df = st.session_state.diamond_data

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

# =================== Página de Inicio ===================
st.markdown("# Bienvenido a Diamond Analytics 🏠")
st.write("Explora los datos y realiza predicciones con modelos de Machine Learning.")

# Header con diseño atractivo
col1, col2 = st.columns([2, 1])
    
with col1:
    st.markdown("<h1 style='color: #3A86FF;'>💎 DIAMOND ANALYTICS</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 20px; color: #555;'>Análisis avanzado y predicción con Machine Learning</p>", unsafe_allow_html=True)

with col2:
    st.image("https://blascojoyero.com/wp-content/uploads/2020/09/diamante-050-blasco-joyero-GVS2-river..jpg", width=200)

st.markdown("---")

# Sección de resumen con KPIs clave
st.subheader("📈 Resumen del Dataset")

# Mostrar KPIs en columnas
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Precio Promedio",
        value=f"${df['price'].mean():,.2f}",
        delta=f"{(df['price'].mean() / df['price'].median() - 1) * 100:.1f}% vs mediana"
    )

with col2:
    st.metric(
        label="Quilates Promedio",
        value=f"{df['carat'].mean():.2f}",
        delta=f"{df['carat'].max():.2f} máx"
    )

with col3:
    corte_top = df['cut'].value_counts().idxmax()
    st.metric(
        label="Corte más común",
        value=f"{corte_top}",
        delta=f"{df['cut'].value_counts()[corte_top] / len(df) * 100:.1f}% del total"
    )

with col4:
    color_top = df['color'].value_counts().idxmax()
    st.metric(
        label="Color predominante",
        value=f"{color_top}",
        delta=f"{df['color'].value_counts()[color_top] / len(df) * 100:.1f}% del total"
    )

# Dashboard principal con tabs para mejor organización
st.markdown("## 🔍 Descubre el mundo de los diamantes")

tab1, tab2, tab3 = st.tabs(["🌟 Proyecto", "📊 Vista Previa", "🧠 Modelos"])

with tab1:
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("""
        ### 🚀 Bienvenido a Diamond Analytics
        
        Este proyecto utiliza **ciencia de datos y aprendizaje automático** para analizar el conjunto de datos `diamonds` de seaborn, que contiene información detallada sobre **53,940 diamantes** con sus características y precios.
        
        💫 **¿Qué hace único a este análisis?**
        - Visualizaciones interactivas con filtros dinámicos
        - Modelos predictivos con métricas en tiempo real
        - Simulador para estimar precios personalizados
        - Insights del mercado basados en datos reales
        
        👨‍💻 **Tecnologías utilizadas:**
        - Python | Pandas | NumPy
        - Scikit-learn | Matplotlib | Seaborn
        - Streamlit | Plotly
        """)
        
        st.info("Navega por las diferentes secciones usando el menú lateral izquierdo para descubrir todos los análisis disponibles.")
    
    with col2:
        # Diagrama de radar mostrando características importantes
        # Datos para gráfico radial
        categories = ['Quilates', 'Profundidad', 'Tabla', 'Precio', 'Dimensión x', 'Dimensión y']
        
        # Normalizar valores para el gráfico radial
        values = [
            df['carat'].mean() / df['carat'].max(),
            df['depth'].mean() / df['depth'].max(),
            df['table'].mean() / df['table'].max(),
            df['price'].mean() / df['price'].max(),
            df['x'].mean() / df['x'].max(),
            df['y'].mean() / df['y'].max()
        ]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            line_color='#3A86FF',
            fillcolor='rgba(58, 134, 255, 0.3)'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )),
            showlegend=False,
            title="Características Promedio (Normalizado)",
            height=350
        )
        
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Vista previa de los datos")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Permitir filtrar por columnas principales
        cortes = st.multiselect("Filtrar por corte:", options=sorted(df['cut'].unique()), default=None)
        precio_rango = st.slider("Rango de precios ($):", min_value=int(df['price'].min()), max_value=int(df['price'].max()), 
                                value=[int(df['price'].min()), int(df['price'].max())])
        
        # Aplicar filtros
        df_filtrado = df.copy()
        if cortes:
            df_filtrado = df_filtrado[df_filtrado['cut'].isin(cortes)]
        df_filtrado = df_filtrado[(df_filtrado['price'] >= precio_rango[0]) & (df_filtrado['price'] <= precio_rango[1])]
        
        # Mostrar conteo
        st.write(f"Mostrando {len(df_filtrado):,} de {len(df):,} diamantes")
    
    with col2:
        # Tabla con estilo mejorado
        st.dataframe(
            df_filtrado.head(10).style.background_gradient(cmap='Blues', subset=['price', 'carat']).format({
                'price': '${:.2f}',
                'carat': '{:.2f}',
                'depth': '{:.1f}%',
                'x': '{:.2f} mm',
                'y': '{:.2f} mm',
                'z': '{:.2f} mm'
            }),
            use_container_width=True
        )
        
        col_stats1, col_stats2 = st.columns(2)
        with col_stats1:
            st.markdown("#### 📋 Tipos de variables")
            st.write(f"**Numéricas:** {df.select_dtypes(include=['float64', 'int64']).columns.tolist()}")
            st.write(f"**Categóricas:** {df.select_dtypes(include=['object', 'category']).columns.tolist()}")
        
        with col_stats2:
            # Mostrar valores faltantes si los hay
            missing = df.isnull().sum()
            if missing.sum() > 0:
                st.markdown("#### 🚫 Valores faltantes")
                st.write(missing[missing > 0])
            else:
                st.markdown("#### ✅ Calidad de datos")
                st.success("¡El dataset está completo! No hay valores faltantes.")

with tab3:
    st.subheader("🤖 Modelos de Machine Learning")
    
    col1, col2 = st.columns(2)
    
    # =================== Modelo de Regresión ===================
    with col1:
        st.markdown("""
        ### 📈 Modelo de Regresión
        
        🔍 **Predice el precio de un diamante** en función de sus características físicas.
        
        **Variables utilizadas:**
        - **Quilates** (Peso en carats)
        - **Dimensiones:** Longitud (x), Ancho (y), Altura (z)
        - **Claridad**
        - **Color**
        - **Proporciones:** Profundidad y Tabla
        
        **Mejor modelo seleccionado:**  
        ✅ **Gradient Boosting Regressor**  
        *(Seleccionado por menor MAE en pruebas de validación)*
        
        📌 *Navega a la sección de Regresión para ver el modelo completo*
        """)
    
    # =================== Modelo de Clasificación ===================
    with col2:
        st.markdown("""
        ### ⚡ Modelo de Clasificación
        
        🔍 **Predice la calidad del corte de un diamante** basado en sus atributos.
        
        **Variables utilizadas:**
        - **Quilates (Peso)**
        - **Dimensiones:** Longitud (x), Ancho (y), Altura (z)
        - **Precio**
        - **Color**
        - **Claridad**
        - **Proporciones:** Profundidad y Tabla
        
        **Mejor modelo seleccionado:**  
        ✅ **Random Forest Classifier**  
        *(Seleccionado por mayor precisión en pruebas de validación)*
        
        📌 *Navega a la sección de Clasificación para ver el modelo completo*
        """)

# Sección de recursos adicionales
st.markdown("---")
st.markdown("## 📚 Recursos y Referencias")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 📗 Documentación
    - [Dataset Diamonds](https://ggplot2.tidyverse.org/reference/diamonds.html)
    - [Guía de diamantes GIA](https://4cs.gia.edu/)
    - [Streamlit Docs](https://docs.streamlit.io/)
    """)

with col2:
    st.markdown("""
    ### 🧰 Herramientas
    - [Pandas](https://pandas.pydata.org/)
    - [Scikit-learn](https://scikit-learn.org/)
    - [Plotly](https://plotly.com/)
    - [Seaborn](https://seaborn.pydata.org/)
    """)

with col3:
    st.markdown("""
    ### 📊 Análisis complementarios
    - [Tendencias de precios de diamantes](https://www.diamonds.pro/education/diamond-prices/)
    - [Factors that Affect Diamond Prices](https://www.gemsociety.org/article/diamond-pricing-analysis/)
    """)

# Call to action
st.markdown("---")
st.success("👈 Selecciona **'📊 Análisis Exploratorio'** en el menú de navegación para comenzar a explorar los datos!")

# Footer con estilo
st.markdown("---")
st.markdown("""
<div style='text-align: center;'>
    <p style='color: #555;'>Desarrollado para el Bootcamp de Data Science 2025</p>
    <p style='color: #777; font-size: 12px;'>Última actualización: Marzo 2025</p>
</div>
""", unsafe_allow_html=True)