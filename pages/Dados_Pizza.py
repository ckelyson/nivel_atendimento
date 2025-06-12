import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("Gráficos de Pizza - Notas de Avaliação por Turno")

# Upload do arquivo Excel
uploaded_file = st.file_uploader("Envie o arquivo Excel", type=["xlsx"])
if uploaded_file is not None:
    # Definir turnos
    turno_a = ["Alison", "Aucimar", "Adilson", "Andre", "Fabiano"]
    turno_b_c = ["Edivan", "Ezequias", "Genivaldo", "João Gomes", "João Vitor", "Leandro", "Obério", "Jhone Kened"]

    # Carregar planilhas
    excel = pd.ExcelFile(uploaded_file)
    sheet_names = excel.sheet_names

    # Selecionar a aba desejada
    selected_sheet = st.selectbox("Selecione a aba (planilha):", sheet_names)

    # Carregar a planilha selecionada
    df = excel.parse(selected_sheet)
    df.columns = df.columns.str.strip()  # remover espaços

    # Verifica se existe a coluna 'Empilhador'
    if "Empilhador" not in df.columns:
        st.error("A coluna 'Empilhador' não foi encontrada. Verifique o nome exato da coluna no seu arquivo.")
    else:
        # Ignorar últimas 4 colunas
        df_notas = df.iloc[:, :-4]

        # Identificar colunas de nota
        nota_cols = [
            col for col in df_notas.columns
            if df_notas[col].dropna().apply(lambda x: isinstance(x, (int, float)) and 0 <= x <= 10).all()
        ]

        # Mapeamento de cores
        def cor_nota(nota):
            if nota == 10:
                return '#2ecc71'  # verde
            elif nota == 9:
                return '#3498db'  # azul
            elif nota == 8:
                return '#f1c40f'  # amarelo
            elif nota == 7:
                return '#e67e22'  # laranja
            else:
                return '#e74c3c'  # vermelho

        # Função para desenhar gráficos por turno
        def desenhar_graficos(df_filtrado, turno_nome):
            st.subheader(f"Turno {turno_nome}")
            colunas = st.columns(3)
            for i, col in enumerate(nota_cols):
                with colunas[i % 3]:
                    counts = df_filtrado[col].value_counts().sort_index()
                    colors = [cor_nota(n) for n in counts.index]
                    fig, ax = plt.subplots()
                    ax.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=90, colors=colors)
                    ax.axis('equal')
                    st.pyplot(fig)
                    st.caption(f"Distribuição de notas para: **{col}**")

        # Filtrar por turno
        df_turno_a = df[df['Empilhador'].isin(turno_a)]
        df_turno_b_c = df[df['Empilhador'].isin(turno_b_c)]

        # Exibir gráficos para cada turno
        desenhar_graficos(df_turno_a, "A")
        desenhar_graficos(df_turno_b_c, "B/C")


