import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("Gráficos de Pizza - Agrupados a cada 3 Notas por Turno")

# Upload do arquivo Excel
uploaded_file = st.file_uploader("Envie o arquivo Excel", type=["xlsx"])
if uploaded_file is not None:
    # Turnos
    turno_a = ["Alison", "Aucimar", "Adilson", "Andre", "Fabiano"]
    turno_b_c = ["Edivan", "Ezequias", "Genivaldo", "João Gomes", "João Vitor", "Leandro", "Obério", "Jhone Kened"]

    # Carregar planilhas
    excel = pd.ExcelFile(uploaded_file)
    sheet_names = excel.sheet_names

    # Selecionar aba
    selected_sheet = st.selectbox("Selecione a aba (planilha):", sheet_names)
    df = excel.parse(selected_sheet)
    df.columns = df.columns.str.strip()

    if "Empilhador:" not in df.columns:
        st.error("A coluna 'Empilhador:' não foi encontrada.")
    else:
        # Ignorar as 4 últimas colunas
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

        # Função para gerar gráficos agrupados de 3 em 3 colunas
        def graficos_por_turno(df_turno, nome_turno):
            st.subheader(f"Turno {nome_turno}")
            for i in range(0, len(nota_cols), 3):
                grupo = nota_cols[i:i+3]
                df_grupo = df_turno[grupo]

                # Agrupar todas as notas das 3 colunas
                notas_agrupadas = df_grupo.values.flatten()
                notas_agrupadas = pd.Series(notas_agrupadas)
                notas_agrupadas = notas_agrupadas[notas_agrupadas.notna()]
                counts = notas_agrupadas.value_counts().sort_index()
                colors = [cor_nota(int(n)) for n in counts.index]

                fig, ax = plt.subplots()
                ax.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=90, colors=colors)
                ax.axis('equal')
                st.pyplot(fig)
                st.caption(f"Distribuição de notas para: {', '.join(grupo)}")

        # Filtrar turnos
        df_turno_a = df[df['Empilhador:'].isin(turno_a)]
        df_turno_b_c = df[df['Empilhador:'].isin(turno_b_c)]

        graficos_por_turno(df_turno_a, "A")
        graficos_por_turno(df_turno_b_c, "B/C")
