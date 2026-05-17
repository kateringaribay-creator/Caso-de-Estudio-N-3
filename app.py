import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# =========================
# 🧠 POO - ANALIZADOR
# =========================
class DataAnalyzer:
    def __init__(self, df):
        self.df = df

    def numeric_vars(self):
        return self.df.select_dtypes(include=np.number).columns.tolist()

    def categorical_vars(self):
        return self.df.select_dtypes(include="object").columns.tolist()


# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Telco Churn EDA", layout="wide")

st.sidebar.title("📊 Menú")
menu = st.sidebar.radio("Selecciona:", ["Home", "Carga de datos", "EDA", "Conclusiones"])

df = None


# =========================
# HOME
# =========================
if menu == "Home":
    st.title("📊 Telco Customer Churn - EDA")

    st.write("""
    Aplicación para análisis exploratorio de datos (EDA)
    enfocada en la fuga de clientes (Churn).
    """)

    st.subheader("👤 Autor")
    st.write("Nombre: TU NOMBRE")
    st.write("Curso: Python for Analytics")
    st.write("Año: 2026")

    st.subheader("🛠 Tecnologías")
    st.write("Python, Pandas, Streamlit, Matplotlib, Seaborn")


# =========================
# CARGA DE DATOS
# =========================
elif menu == "Carga de datos":

    st.title("📂 Carga del dataset")

    file = st.file_uploader("Sube el archivo TelcoCustomerChurn.csv", type="csv")

    if file is not None:
        df = pd.read_csv(file)

        # 🔥 LIMPIEZA CLAVE
        df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
        df = df.dropna(subset=["TotalCharges"])

        st.session_state["df"] = df

        st.success("Dataset cargado correctamente ✅")

        st.dataframe(df.head())
        st.write("Dimensiones:", df.shape)

    else:
        st.info("Sube el archivo para comenzar")


# =========================
# EDA
# =========================
elif menu == "EDA":

    st.title("📊 Análisis Exploratorio de Datos")

    if "df" not in st.session_state:
        st.warning("Primero carga el dataset ⚠️")

    else:
        df = st.session_state["df"]
        analyzer = DataAnalyzer(df)

        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "Info",
            "Variables",
            "Estadísticas",
            "Missing",
            "Churn Analysis"
        ])

        # -------------------------
        # 1. INFO
        # -------------------------
        with tab1:
            st.subheader("Información general")
            st.text(df.info())
            st.write(df.dtypes)

        # -------------------------
        # 2. VARIABLES
        # -------------------------
        with tab2:
            st.subheader("Clasificación de variables")

            st.write("Numéricas:", analyzer.numeric_vars())
            st.write("Categóricas:", analyzer.categorical_vars())

        # -------------------------
        # 3. ESTADÍSTICAS
        # -------------------------
        with tab3:
            st.subheader("Estadísticas descriptivas")
            st.dataframe(df.describe())

        # -------------------------
        # 4. MISSING
        # -------------------------
        with tab4:
            st.subheader("Valores faltantes")
            st.bar_chart(df.isnull().sum())

        # -------------------------
        # 5. CHURN ANALYSIS
        # -------------------------
        with tab5:
            st.subheader("Análisis de Churn")

            col = st.selectbox("Selecciona variable", df.columns)

            st.bar_chart(df[col].value_counts())

            # Tenure vs Churn
            if "tenure" in df.columns:
                fig, ax = plt.subplots()
                sns.boxplot(data=df, x="Churn", y="tenure", ax=ax)
                st.pyplot(fig)

            # MonthlyCharges vs Churn
            if "MonthlyCharges" in df.columns:
                fig, ax = plt.subplots()
                sns.boxplot(data=df, x="Churn", y="MonthlyCharges", ax=ax)
                st.pyplot(fig)

            # Contract vs Churn
            if "Contract" in df.columns:
                fig, ax = plt.subplots()
                sns.countplot(data=df, x="Contract", hue="Churn", ax=ax)
                plt.xticks(rotation=45)
                st.pyplot(fig)


# =========================
# CONCLUSIONES
# =========================
elif menu == "Conclusiones":

    st.title("📌 Conclusiones")

    st.write("""
    1. Los clientes con contratos mensuales presentan mayor churn.
    2. Los clientes nuevos abandonan más el servicio.
    3. Mayor cargo mensual incrementa la probabilidad de fuga.
    4. El tipo de contrato influye en la retención.
    5. La empresa debe mejorar estrategias de fidelización.
    """)