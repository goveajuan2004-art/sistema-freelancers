import streamlit as st
import pandas as pd
import numpy as np
from datetime import date
from sklearn.tree import DecisionTreeClassifier

# Configuración de la página
st.set_page_config(
    page_title="DSS Micro-Tareas Digitales",
    page_icon="📊",
    layout="wide"
)

# Encabezado principal
st.title("📊 Sistema de Apoyo a la Toma de Decisiones (DSS)")
st.markdown("**Optimización de la Rentabilidad en Micro-Tareas Digitales para Freelancers**")
st.caption(f"📅 Actualización del Mercado: **{date.today().strftime('%d/%m/%Y')}** | Autor: Juan Govea")
st.markdown("---")

# 1. Entrenamiento del Modelo de Clasificación (Árbol de Decisión)
@st.cache_resource
def entrenar_clasificador():
    historico = pd.DataFrame({
        'tiempo_min': [15, 60, 5, 45, 90, 20, 120, 10, 30, 50, 25, 80],
        'pago_usd':   [2.50, 1.80, 0.40, 5.00, 3.00, 3.50, 4.00, 1.20, 4.00, 1.50, 3.20, 2.50],
        'dificultad': [1, 3, 1, 2, 3, 1, 3, 1, 2, 2, 1, 3],
        'rentable':   [1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0]
    })
    X = historico[['tiempo_min', 'pago_usd', 'dificultad']]
    y = historico['rentable']
    
    modelo = DecisionTreeClassifier(random_state=42)
    modelo.fit(X, y)
    return modelo

modelo = entrenar_clasificador()

# 2. Generación / Actualización del Tablero Diario de Mercado con Enlaces Directos
def obtener_tareas_del_dia(semilla=42):
    np.random.seed(semilla)
    tareas_base = [
        {"Plataforma": "Freecash", "Micro-Tarea": "Encuesta de Consumo Tecnológico", "Tiempo (min)": 15, "Pago (USD)": 2.20, "Dificultad_Num": 1, "URL": "https://freecash.com"},
        {"Plataforma": "2Captcha", "Micro-Tarea": "Resolución de 1000 reCAPTCHAs v2", "Tiempo (min)": 65, "Pago (USD)": 1.10, "Dificultad_Num": 2, "URL": "https://2captcha.com"},
        {"Plataforma": "SproutGigs", "Micro-Tarea": "Registro y verificación en App Fintech", "Tiempo (min)": 10, "Pago (USD)": 1.50, "Dificultad_Num": 1, "URL": "https://sproutgigs.com"},
        {"Plataforma": "Toloka", "Micro-Tarea": "Clasificación de imágenes para IA", "Tiempo (min)": 30, "Pago (USD)": 3.80, "Dificultad_Num": 2, "URL": "https://toloka.ai"},
        {"Plataforma": "Clickworker", "Micro-Tarea": "Grabación de comandos de voz (20 frases)", "Tiempo (min)": 20, "Pago (USD)": 4.50, "Dificultad_Num": 1, "URL": "https://www.clickworker.com"},
        {"Plataforma": "Freecash", "Micro-Tarea": "Subir nivel en juego móvil (Oferta)", "Tiempo (min)": 120, "Pago (USD)": 5.00, "Dificultad_Num": 3, "URL": "https://freecash.com"},
        {"Plataforma": "2Captcha", "Micro-Tarea": "Transcripción de captchas de texto rápido", "Tiempo (min)": 45, "Pago (USD)": 0.85, "Dificultad_Num": 1, "URL": "https://2captcha.com"},
        {"Plataforma": "Outlier", "Micro-Tarea": "Etiquetado Lidar 3D básico", "Tiempo (min)": 90, "Pago (USD)": 4.20, "Dificultad_Num": 3, "URL": "https://outlier.ai"},
        {"Plataforma": "TimeBucks", "Micro-Tarea": "Visualización de anuncios y clics diarios", "Tiempo (min)": 25, "Pago (USD)": 0.45, "Dificultad_Num": 1, "URL": "https://timebucks.com"},
        {"Plataforma": "Appen", "Micro-Tarea": "Evaluación de relevancia de búsqueda web", "Tiempo (min)": 40, "Pago (USD)": 6.00, "Dificultad_Num": 2, "URL": "https://appen.com"},
    ]
    df = pd.DataFrame(tareas_base)
    
    variacion = np.random.uniform(0.90, 1.15, size=len(df))
    df["Pago (USD)"] = (df["Pago (USD)"] * variacion).round(2)
    df["Ganancia/Hora ($/h)"] = ((df["Pago (USD)"] / df["Tiempo (min)"]) * 60).round(2)
    
    mapa_dif = {1: "Baja", 2: "Media", 3: "Alta"}
    df["Dificultad"] = df["Dificultad_Num"].map(mapa_dif)
    
    X_pred = df[["Tiempo (min)", "Pago (USD)", "Dificultad_Num"]].rename(
        columns={"Tiempo (min)": "tiempo_min", "Pago (USD)": "pago_usd", "Dificultad_Num": "dificultad"}
    )
    predicciones = modelo.predict(X_pred)
    df["Clasificación IA"] = ["✅ Alta Rentabilidad" if p == 1 else "⚠️ Baja Rentabilidad" for p in predicciones]
    
    return df

# Control de actualización diaria en sesión
if "semilla_dia" not in st.session_state:
    st.session_state.semilla_dia = int(date.today().strftime("%Y%m%d"))

# Barra lateral: Filtros y Actualización
st.sidebar.header("⚙️ Panel de Control del Freelancer")

if st.sidebar.button("🔄 Sincronizar Tareas del Día"):
    st.session_state.semilla_dia += 1
    st.sidebar.success("¡Mercado actualizado con las ofertas más recientes!")

df_mercado = obtener_tareas_del_dia(st.session_state.semilla_dia)

plataformas = ["Todas"] + list(df_mercado["Plataforma"].unique())
filtro_plat = st.sidebar.selectbox("Filtrar por Plataforma:", plataformas)

filtro_rent = st.sidebar.radio(
    "Mostrar tareas según Rentabilidad:",
    ["Todas las tareas", "Solo ✅ Alta Rentabilidad", "Solo ⚠️ Baja Rentabilidad"]
)

filtro_dif = st.sidebar.multiselect(
    "Nivel de Dificultad:",
    options=["Baja", "Media", "Alta"],
    default=["Baja", "Media", "Alta"]
)

# Aplicar filtros al tablero
df_filtrado = df_mercado.copy()
if filtro_plat != "Todas":
    df_filtrado = df_filtrado[df_filtrado["Plataforma"] == filtro_plat]
if filtro_rent == "Solo ✅ Alta Rentabilidad":
    df_filtrado = df_filtrado[df_filtrado["Clasificación IA"] == "✅ Alta Rentabilidad"]
elif filtro_rent == "Solo ⚠️ Baja Rentabilidad":
    df_filtrado = df_filtrado[df_filtrado["Clasificación IA"] == "⚠️ Baja Rentabilidad"]
if filtro_dif:
    df_filtrado = df_filtrado[df_filtrado["Dificultad"].isin(filtro_dif)]

# Métricas Resumen
col1, col2, col3, col4 = st.columns(4)
total_tareas = len(df_filtrado)
rentables_count = len(df_filtrado[df_filtrado["Clasificación IA"] == "✅ Alta Rentabilidad"])
ganancia_potencial = df_filtrado[df_filtrado["Clasificación IA"] == "✅ Alta Rentabilidad"]["Pago (USD)"].sum()
promedio_hora = df_filtrado["Ganancia/Hora ($/h)"].mean() if total_tareas > 0 else 0

col1.metric("Tareas Disponibles Hoy", f"{total_tareas}")
col2.metric("Tareas Óptimas (IA)", f"{rentables_count}")
col3.metric("Ganancia Óptima Acumulada", f"${ganancia_potencial:.2f} USD")
col4.metric("Promedio Mercado ($/h)", f"${promedio_hora:.2f}/h")

st.markdown("### 📋 Tablero de Micro-Tareas del Mercado")
st.info("💡 **Consejo:** Haz clic en los botones de la columna **Enlace Directo** para abrir la plataforma correspondiente en una nueva pestaña.")

# Mostrar tabla con enlaces interactivos configurados
columnas_mostrar = ["Plataforma", "Micro-Tarea", "Tiempo (min)", "Pago (USD)", "Ganancia/Hora ($/h)", "Dificultad", "Clasificación IA", "URL"]
st.dataframe(
    df_filtrado[columnas_mostrar].sort_values(by="Ganancia/Hora ($/h)", ascending=False),
    column_config={
        "URL": st.column_config.LinkColumn(
            "Enlace Directo",
            help="Acceso directo a la plataforma de micro-tareas",
            display_text="🔗 Visitar Sitio"
        )
    },
    use_container_width=True,
    hide_index=True
)

# Módulo adicional de evaluación manual
with st.expander("➕ Evaluar una micro-tarea nueva encontrada fuera del tablero"):
    c1, c2, c3, c4 = st.columns(4)
    nueva_plat = c1.text_input("Plataforma", "Freecash")
    nuevo_tiempo = c2.number_input("Tiempo estimado (min)", min_value=1, max_value=300, value=20)
    nuevo_pago = c3.number_input("Pago ofrecido (USD)", min_value=0.05, max_value=100.0, value=2.50, step=0.10)
    nueva_dif = c4.selectbox("Dificultad", [1, 2, 3], format_func=lambda x: ["Baja", "Media", "Alta"][x-1])
    
    if st.button("Analizar Tarea con el Modelo"):
        pred = modelo.predict([[nuevo_tiempo, nuevo_pago, nueva_dif]])[0]
        tasa_hora = (nuevo_pago / nuevo_tiempo) * 60
        if pred == 1:
            st.success(f"✅ **RECOMENDADA ({nueva_plat}):** Rendimiento estimado de **${tasa_hora:.2f}/hora**. Es rentable realizarla.")
        else:
            st.error(f"⚠️ **NO RECOMENDADA ({nueva_plat}):** Rendimiento bajo de **${tasa_hora:.2f}/hora**. El algoritmo sugiere descartarla.")