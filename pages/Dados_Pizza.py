import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("Gráficos de Pizza - Notas de Avaliação")

# Upload do arquivo Excel
uploaded_file = st.file_uploader("Envie o arquivo Excel", type=["xlsx"])
if uploaded_file is not None:
    # Carregar planilhas
    excel = pd.ExcelFile(uploaded_file)
    sheet_names = excel.sheet_names

    for sheet in sheet_names:
        st.header(f"Avaliações - {sheet}")
        df = excel.parse(sheet)

        # Normalizar nomes das colunas (remover espaços extras, etc.)
        df.columns = df.columns.str.strip()

        # Identificar colunas com notas de 0 a 10
        nota_cols = [
            col for col in df.columns
            if df[col].dropna().apply(lambda x: isinstance(x, (int, float)) and 0 <= x <= 10).all()
        ]

        colunas = st.columns(3)
        for i, col in enumerate(nota_cols):
            with colunas[i % 3]:
                counts = df[col].value_counts().sort_index()
                fig, ax = plt.subplots()
                ax.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=90)
                ax.axis('equal')
                st.pyplot(fig)
                st.caption(f"Distribuição de notas para: **{col}**")
