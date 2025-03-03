import streamlit as st
import seaborn as sns
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt

# =================== Cargar el Dataset desde session_state ===================
if "diamond_data" in st.session_state:
    df = st.session_state.diamond_data
else:
    st.error("⚠️ Error: No se ha encontrado el dataset. Regresa a la página de inicio.")
    st.stop()  # Detener la ejecución para evitar errores
    

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

# =================== Análisis Exploratorio ===================

st.title("📊 Análisis Exploratorio de Datos")
    
# Banner estilizado con gradiente
st.markdown("""
<div style="background: linear-gradient(to right, #4364f7, #6fb1fc); padding: 15px; border-radius: 10px; margin-bottom: 20px;">
    <h2 style="color: white; margin: 0;">🔍 Explorando los Factores que Afectan los Diamantes</h2>
</div>
""", unsafe_allow_html=True)

# Descripción mejorada
st.markdown("""
En esta sección analizaremos de forma visual los factores que impactan en el **precio** (`price`) 
y la **calidad del corte** (`cut`) de los diamantes. Los gráficos interactivos te permitirán
descubrir patrones clave en los datos y comprender mejor las relaciones entre las variables.

Utiliza los filtros en el panel lateral para personalizar tu análisis 👉
""")

# Formulario de filtros con diseño mejorado
with st.form("filters_form"):
    # Mejora visual de los controles con emojis y colores
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<p style="color: #4364f7; font-weight: bold;">💎 Características</p>', unsafe_allow_html=True)
        cut_filter = st.multiselect("Tipo de Corte", df["cut"].unique(), default=df["cut"].unique())
        clarity_filter = st.multiselect("Claridad", df["clarity"].unique(), default=df["clarity"].unique())
    
    with col2:
        st.markdown('<p style="color: #4364f7; font-weight: bold;">🔍 Propiedades</p>', unsafe_allow_html=True)
        color_filter = st.multiselect("Color", df["color"].unique(), default=df["color"].unique())
        carat_range = st.slider("Rango de Quilates", 
                                float(df["carat"].min()), 
                                float(df["carat"].max()), 
                                (float(df["carat"].min()), float(df["carat"].max())))
    
    # Botón con estilo
    submitted = st.form_submit_button("Aplicar Filtros", 
                                        use_container_width=True)

# Filtrado de Datos
df_filtered = df[
    (df["cut"].isin(cut_filter)) &
    (df["color"].isin(color_filter)) &
    (df["clarity"].isin(clarity_filter)) &
    (df["carat"] >= carat_range[0]) & (df["carat"] <= carat_range[1])
]

# Métricas destacadas
st.markdown("### 📌 Resumen de Datos Filtrados")

# Mostrar métricas clave en forma de tarjetas
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Total de Diamantes", 
                value=f"{len(df_filtered):,}", 
                delta=f"{len(df_filtered)/len(df)*100:.1f}% del total")
with col2:
    st.metric(label="Precio Promedio", 
                value=f"${df_filtered['price'].mean():,.2f}")
with col3:
    st.metric(label="Quilates Promedio", 
                value=f"{df_filtered['carat'].mean():.2f}")

# Dataframe más compacto sin estilo para evitar el error de límite de celdas
with st.expander("Ver datos filtrados", expanded=False):
    st.dataframe(df_filtered, use_container_width=True, height=250)

# Separador estilizado
st.markdown("""<hr style="height:2px;border:none;color:#4364f7;background-color:#4364f7;margin:25px 0;" />""", 
            unsafe_allow_html=True)

# Distribución de precios con tema coherente
st.subheader("💰 Distribución de Precios")

# Tabs para ofrecer diferentes visualizaciones
precio_tab1, precio_tab2 = st.tabs(["Histograma (Plotly)", "Histograma (Seaborn)"])

with precio_tab1:
    fig = px.histogram(df_filtered, x="price", 
                        color_discrete_sequence=["#4364f7"],
                        marginal="box",
                        nbins=30,
                        opacity=0.7,
                        title="Distribución de precios de los diamantes")
    fig.update_layout(
        plot_bgcolor="white",
        xaxis_title="Precio ($)",
        yaxis_title="Cantidad de diamantes",
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

with precio_tab2:
    # Gráfica de Seaborn - Histograma estilizado
    st.markdown('<p style="color: #4364f7; font-weight: bold; font-size: 14px;">Gráfico generado con Seaborn</p>', unsafe_allow_html=True)
    
    # Configuración de estilo de seaborn para mantener consistencia con el diseño
    sns.set_style("whitegrid")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Histograma con KDE
    sns.histplot(df_filtered["price"], bins=30, kde=True, color="#4364f7", alpha=0.7, ax=ax)
    
    # Personalización para que combine con el diseño
    ax.set_title("Distribución del Precio de los Diamantes", fontsize=16, pad=20)
    ax.set_xlabel("Precio ($)", fontsize=12)
    ax.set_ylabel("Frecuencia", fontsize=12)
    
    # Mejorar apariencia general
    plt.tight_layout()
    
    # Mostrar el gráfico
    st.pyplot(fig)

# Relación entre quilates y precio con mejor presentación
st.markdown("""<div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; margin: 20px 0;">
            <h3 style="margin-top: 0;">📈 Relación entre Quilates y Precio</h3>
            </div>""", 
            unsafe_allow_html=True)

scatter_tab1, scatter_tab2 = st.tabs(["Plotly Interactivo", "Seaborn"])

with scatter_tab1:
    color_var = st.radio("Colorear por:", ["cut", "color", "clarity"], horizontal=True)
    
    fig = px.scatter(df_filtered, 
                    x="carat", 
                    y="price", 
                    color=color_var,
                    size="depth",
                    hover_name="cut",
                    hover_data=["clarity", "color", "table"],
                    title="Relación entre quilates y precio",
                    color_discrete_sequence=px.colors.qualitative.Bold,
                    opacity=0.7,
                    trendline="ols")
    
    fig.update_layout(
        plot_bgcolor="white",
        xaxis_title="Quilates",
        yaxis_title="Precio ($)",
        height=500,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    st.plotly_chart(fig, use_container_width=True)

with scatter_tab2:
    st.markdown('<p style="color: #4364f7; font-weight: bold; font-size: 14px;">Gráfico generado con Seaborn</p>', unsafe_allow_html=True)
    
    # Configurar un estilo limpio para Seaborn
    sns.set_style("whitegrid")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Si hay demasiados puntos, tomamos una muestra para no sobrecargar la visualización
    sample_size = min(5000, len(df_filtered))
    sampled_data = df_filtered.sample(sample_size, random_state=42) if len(df_filtered) > sample_size else df_filtered
    
    # Gráfico de dispersión con regresión
    sns.regplot(
        x="carat", 
        y="price", 
        data=sampled_data, 
        scatter_kws={"alpha": 0.6, "color": "#4364f7"}, 
        line_kws={"color": "#ff6b6b"},
        ax=ax
    )
    
    # Overlay con un scatterplot coloreado por tipo de corte
    sns.scatterplot(
        x="carat", 
        y="price", 
        hue="cut", 
        data=sampled_data, 
        alpha=0.6, 
        palette="coolwarm",
        ax=ax
    )
    
    # Personalización visual
    ax.set_title("Relación entre Quilates y Precio por Tipo de Corte", fontsize=16, pad=20)
    ax.set_xlabel("Quilates", fontsize=12)
    ax.set_ylabel("Precio ($)", fontsize=12)
    
    # Ajustar leyenda
    plt.legend(title="Tipo de Corte", bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # Ajustar diseño
    plt.tight_layout()
    
    # Mostrar el gráfico
    st.pyplot(fig)

# Comparativa de precios por tipo de corte
st.markdown("""<div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; margin: 20px 0;">
            <h3 style="margin-top: 0;">📊 Análisis Comparativo</h3>
            </div>""", 
            unsafe_allow_html=True)

comparativa_tab1, comparativa_tab2 = st.tabs(["Plotly", "Seaborn"])

with comparativa_tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.box(df_filtered, 
                    x="cut", 
                    y="price", 
                    color="cut",
                    title="Precio según tipo de corte",
                    color_discrete_sequence=px.colors.qualitative.Bold)
        fig.update_layout(
            plot_bgcolor="white",
            xaxis_title="Tipo de corte",
            yaxis_title="Precio ($)",
            showlegend=False,
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.box(df_filtered, 
                    x="color", 
                    y="price", 
                    color="color",
                    title="Precio según color",
                    color_discrete_sequence=px.colors.qualitative.Bold)
        fig.update_layout(
            plot_bgcolor="white",
            xaxis_title="Color",
            yaxis_title="Precio ($)",
            showlegend=False,
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

with comparativa_tab2:
    st.markdown('<p style="color: #4364f7; font-weight: bold; font-size: 14px;">Gráficos generados con Seaborn</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Boxplot con Seaborn para Cut
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Personalizar la apariencia de seaborn
        sns.set_style("whitegrid")
        sns.set_palette("coolwarm")
        
        # Crear boxplot
        sns.boxplot(x="cut", y="price", data=df_filtered, ax=ax, palette="coolwarm")
        
        # Añadir swarmplot con puntos para mejor visualización de la distribución
        sns.swarmplot(x="cut", y="price", data=df_filtered.sample(min(500, len(df_filtered))), 
                        color="black", alpha=0.5, ax=ax, size=3)
        
        # Personalización visual
        ax.set_title("Precio según Tipo de Corte", fontsize=14, pad=20)
        ax.set_xlabel("Tipo de Corte", fontsize=12)
        ax.set_ylabel("Precio ($)", fontsize=12)
        plt.xticks(rotation=45)
        
        # Ajustar diseño
        plt.tight_layout()
        
        # Mostrar el gráfico
        st.pyplot(fig)
        
    with col2:
        # Violinplot con Seaborn para Clarity
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Crear violinplot
        sns.violinplot(x="clarity", y="price", data=df_filtered, ax=ax, palette="viridis")
        
        # Personalización visual
        ax.set_title("Distribución de Precios por Claridad", fontsize=14, pad=20)
        ax.set_xlabel("Claridad", fontsize=12)
        ax.set_ylabel("Precio ($)", fontsize=12)
        plt.xticks(rotation=45)
        
        # Ajustar diseño
        plt.tight_layout()
        
        # Mostrar el gráfico
        st.pyplot(fig)

# Matriz de correlación mejorada
st.markdown("""<div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; margin: 20px 0;">
            <h3 style="margin-top: 0;">📉 Correlaciones entre Variables</h3>
            </div>""", 
            unsafe_allow_html=True)

corr_tab1, corr_tab2 = st.tabs(["Plotly", "Seaborn"])

with corr_tab1:
    # Matriz con heatmap interactivo de Plotly
    corr_matrix = df_filtered.select_dtypes(include=['number']).corr()
    fig = px.imshow(corr_matrix, 
                    text_auto='.2f',
                    color_continuous_scale='RdBu_r',
                    title="Matriz de Correlación entre Variables Numéricas",
                    aspect="auto")
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

with corr_tab2:
    st.markdown('<p style="color: #4364f7; font-weight: bold; font-size: 14px;">Gráfico generado con Seaborn</p>', unsafe_allow_html=True)
    
    # Heatmap de correlación con Seaborn
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Calcular correlación
    corr_matrix = df_filtered.select_dtypes(include=['number']).corr()
    
    # Crear máscara para triángulo superior
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    
    # Crear heatmap con máscara
    sns.heatmap(corr_matrix, 
                annot=True, 
                fmt='.2f', 
                cmap='coolwarm', 
                mask=mask, 
                linewidths=0.5, 
                cbar_kws={"shrink": 0.8},
                ax=ax)
    
    # Personalización
    ax.set_title("Matriz de Correlación (Triángulo Inferior)", fontsize=16, pad=20)
    
    # Ajustar diseño
    plt.tight_layout()
    
    # Mostrar el gráfico
    st.pyplot(fig)

# Añadir gráfico de pares con Seaborn
st.markdown("""<div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; margin: 20px 0;">
            <h3 style="margin-top: 0;">🔄 Relaciones Multivariables (Seaborn)</h3>
            </div>""", 
            unsafe_allow_html=True)

# Seleccionar variables para el pairplot
st.markdown('<p style="color: #4364f7; font-weight: bold; font-size: 14px;">Selecciona variables para el análisis de pares</p>', unsafe_allow_html=True)
pairplot_vars = st.multiselect(
    "Variables a incluir:", 
    options=['carat', 'depth', 'table', 'price', 'x', 'y', 'z'],
    default=['carat', 'price', 'depth']
)

if len(pairplot_vars) >= 2:
    # Mostrar advertencia si hay muchos datos
    if len(df_filtered) > 1000:
        st.warning("⚠️ Se tomará una muestra de 1000 diamantes para generar el pairplot y mantener un buen rendimiento.")
        df_sample = df_filtered.sample(1000, random_state=42)
    else:
        df_sample = df_filtered
    
    # Color del pairplot
    color_var = st.radio("Variable de color para el pairplot:", ["cut", "clarity", "color"], horizontal=True)
    
    # Crear pairplot
    fig = plt.figure(figsize=(12, 10))
    
    # Configurar estilo
    sns.set_style("whitegrid")
    
    # Generar pairplot
    g = sns.pairplot(
        df_sample, 
        vars=pairplot_vars, 
        hue=color_var, 
        palette="coolwarm", 
        diag_kind="kde",
        plot_kws={'alpha': 0.6, 's': 30, 'edgecolor': 'k', 'linewidth': 0.5},
        diag_kws={'alpha': 0.6, 'fill': True}
    )
    
    # Personalizar título
    g.fig.suptitle(f"Relaciones entre variables seleccionadas (coloreado por {color_var})", 
                    fontsize=16, y=1.02)
    
    # Mostrar pairplot
    st.pyplot(g.fig)
else:
    st.info("ℹ️ Selecciona al menos 2 variables para generar el pairplot.")

# Análisis adicional con KDE bivariado
st.markdown("""<div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; margin: 20px 0;">
            <h3 style="margin-top: 0;">🌊 Densidad Bivariada (Seaborn)</h3>
            </div>""", 
            unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    x_var = st.selectbox("Variable X para densidad:", ["carat", "depth", "table", "price", "x", "y", "z"], index=0)
with col2:
    y_var = st.selectbox("Variable Y para densidad:", ["carat", "depth", "table", "price", "x", "y", "z"], index=3)

if x_var != y_var:
    # Configuración del gráfico
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Configurar estilo
    sns.set_style("whitegrid")
    
    # Si hay muchos puntos, tomar muestra
    if len(df_filtered) > 2000:
        df_sample = df_filtered.sample(2000, random_state=42)
    else:
        df_sample = df_filtered
    
    # Crear KDE bivariado
    sns.kdeplot(
        data=df_sample,
        x=x_var,
        y=y_var,
        fill=True,
        cmap="Blues",
        thresh=0.05,
        alpha=0.7,
        ax=ax
    )
    
    # Superponer scatterplot
    sns.scatterplot(
        data=df_sample,
        x=x_var,
        y=y_var,
        hue="cut",
        palette="coolwarm",
        alpha=0.6,
        ax=ax
    )
    
    # Personalización
    ax.set_title(f"Densidad Bivariada: {x_var} vs {y_var}", fontsize=16, pad=20)
    ax.set_xlabel(x_var, fontsize=12)
    ax.set_ylabel(y_var, fontsize=12)
    
    # Ajustar leyenda
    plt.legend(title="Tipo de Corte", bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # Ajustar diseño
    plt.tight_layout()
    
    # Mostrar el gráfico
    st.pyplot(fig)
else:
    st.info("ℹ️ Selecciona variables diferentes para X e Y para generar el gráfico de densidad.")

# Sección final con insights y conclusiones
st.markdown("""
<div style="background: linear-gradient(to right, #4364f7, #6fb1fc); padding: 15px; border-radius: 10px; margin: 20px 0;">
    <h3 style="color: white; margin: 0;">💡 Principales Hallazgos</h3>
</div>
""", unsafe_allow_html=True)

# Insights automáticos basados en los datos filtrados
st.markdown(f"""
- El **precio promedio** de los diamantes seleccionados es de **${df_filtered['price'].mean():,.2f}**
- La **correlación** entre quilates y precio es de **{df_filtered[['carat', 'price']].corr().iloc[0,1]:.2f}**
- Los diamantes de corte '{df_filtered.groupby('cut')['price'].mean().idxmax()}' tienen el precio promedio más alto
- Los diamantes de color '{df_filtered.groupby('color')['price'].mean().idxmax()}' son los más valiosos en promedio
- La claridad tiene un impacto de **{abs(df_filtered.groupby('clarity')['price'].mean().max() - df_filtered.groupby('clarity')['price'].mean().min()) / df_filtered['price'].mean() * 100:.1f}%** en la variación de precios

Continúa tu exploración en las siguientes secciones para ver los modelos predictivos.
""")

# =================== Footer ===================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #555; font-size: 14px;'>
     Desarrollado para el Bootcamp Data Science 2025 
    <p style='color: #777; font-size: 12px;'>Última actualización: Marzo 2025</p>
</div>
""", unsafe_allow_html=True)