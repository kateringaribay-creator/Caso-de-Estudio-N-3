import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# =========================
# 🧠 CLASE (POO)
# =========================
class DataAnalyzer:
    def __init__(self, df):
        self.df = df

    def info_data(self):
        return self.df.info()

    def describe_data(self):
        return self.df.describe()

    def missing_values(self):
        return self.df.isnull().sum()

    def numeric_columns(self):
        return self.df.select_dtypes(include=np.number).columns.tolist()

    def categorical_columns(self):
        return self.df.select_dtypes(exclude=np.number).columns.tolist()


# =========================
# 🖥️ CONFIG APP
# =========================
st.set_page_config(page_title="EDA Insurance", layout="wide")

st.title("📊 Insurance Company - EDA Streamlit App")

# =========================
# 📂 CARGA DE DATASET
# =========================
uploaded_file = st.file_uploader("📁 Carga el archivo CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    analyzer = DataAnalyzer(df)

    st.success("Archivo cargado correctamente ✅")

    # =========================
    # 🏠 HOME
    # =========================
    st.sidebar.title("Menú")
    option = st.sidebar.selectbox(
        "Selecciona una sección",
        ["Home", "Dataset", "EDA"]
    )

    if option == "Home":
        st.header("🏠 Presentación del proyecto")
        st.write("""
        Este proyecto realiza un Análisis Exploratorio de Datos (EDA)
        sobre una compañía de seguros usando Streamlit.
        """)

        st.write("👨‍💻 Autor: KATERIN DELFINA GARIBAY FERNANDEZ")
        st.write("📘 Curso: Python for Analytics")
        st.write("📅 Año: 2026")

    # =========================
    # 📊 DATASET
    # =========================
    elif option == "Dataset":
        st.header("📂 Vista del Dataset")

        st.write("🔹 Primeras filas:")
        st.dataframe(df.head())

        st.write("🔹 Dimensiones:")
        st.write(df.shape)

    # =========================
    # 📊 EDA
    # =========================
    elif option == "EDA":
        st.header("📊 Análisis Exploratorio de Datos")

        tab1, tab2, tab3, tab4, tab5 = st.tabs(
            ["Info", "Variables", "Estadísticas", "Visualización", "Insights"]
        )

        # ================= INFO =================
        with tab1:
            st.subheader("📌 Información del dataset")
            st.write(df.info())

            st.write("🔹 Valores nulos:")
            st.dataframe(analyzer.missing_values())

        # ================= VARIABLES =================
        with tab2:
            st.subheader("📌 Tipos de variables")

            st.write("🔢 Numéricas:")
            st.write(analyzer.numeric_columns())

            st.write("🔤 Categóricas:")
            st.write(analyzer.categorical_columns())

        # ================= ESTADÍSTICAS =================
        with tab3:
            st.subheader("📌 Estadísticas descriptivas")
            st.dataframe(analyzer.describe_data())

        # ================= VISUALIZACIÓN =================
        with tab4:
            st.subheader("📊 Distribuciones")

            num_cols = analyzer.numeric_columns()

            col = st.selectbox("Selecciona variable numérica", num_cols)

            fig, ax = plt.subplots()
            sns.histplot(df[col], kde=True, ax=ax)
            st.pyplot(fig)

        # ================= INSIGHTS =================
        with tab5:
            st.subheader("🧠 Hallazgos clave")

            st.write("""
            - Se identifican variables con valores faltantes.
            - Existen diferencias entre variables numéricas y categóricas.
            - Algunas variables influyen en el comportamiento del cliente.
            - La visualización ayuda a entender la distribución de datos.
            - El EDA permite generar insights para decisiones de negocio.
            """)

else:
    st.warning("Por favor carga un archivo CSV para comenzar.")
