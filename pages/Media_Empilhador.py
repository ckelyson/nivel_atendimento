import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Média dos Indicadores por Empilhador", layout="wide")
st.title("📊 Média de Produtividade, Qualidade e Segurança por Empilhador")

uploaded_file = st.file_uploader("📂 Envie o arquivo Excel (.xlsx)", type=["xlsx"])

if uploaded_file:
    # Lê todas as abas disponíveis no Excel
    xl = pd.ExcelFile(uploaded_file, engine='openpyxl')
    abas = xl.sheet_names
    aba_selecionada = st.selectbox("🗂️ Selecione a planilha", abas)
    
    df = xl.parse(aba_selecionada)
    df.columns = df.columns.str.strip()

    # Renomeia colunas
    df = df.rename(columns={
        "Líder de manufatura": "Líder",
        "Empilhador:": "Empilhador"
    })

    # Indicadores desejados
    indicadores = ["Produtividade", "Qualidade", "Segurança"]

    # Listas dos empilhadores por turno
    turno_a = ["Alison", "Aucimar", "Adilson", "Andre", "Fabiano"]
    turno_b_c = ["Edivan", "Ezequias", "Genivaldo", "João Gomes", "João Vitor", "Leandro", "Obério", "Jhone Kened"]

    # Calcula média por empilhador (todos)
    media_empilhador = df.groupby("Empilhador")[indicadores].mean().reset_index()
    media_empilhador["Média Total"] = media_empilhador[indicadores].mean(axis=1)

    # Tabela geral formatada
    st.subheader("📋 Média Total por Empilhador")
    media_formatada_total = media_empilhador.copy()
    for col in indicadores + ["Média Total"]:
        media_formatada_total[col] = media_formatada_total[col].map(lambda x: f"{x:.1%}")
    st.dataframe(media_formatada_total)

    # Função para gerar gráfico e tabela por turno
    def gerar_grafico_por_turno(nome_turno, lista_empilhadores):
        df_turno = df[df["Empilhador"].isin(lista_empilhadores)]
        media_turno = df_turno.groupby("Empilhador")[indicadores].mean()

        # Garante que todos os empilhadores do turno apareçam
        media_turno = media_turno.reindex(lista_empilhadores).reset_index()
        media_turno["Média Total"] = media_turno[indicadores].mean(axis=1)

        # Dados para gráfico
        df_melted = media_turno.melt(
            id_vars="Empilhador",
            value_vars=indicadores,
            var_name="Indicador",
            value_name="Porcentagem"
        )
        df_melted["Texto"] = df_melted["Porcentagem"].apply(
            lambda x: f"{x:.1%}" if pd.notna(x) else "N/A"
        )

        # Cores dos indicadores
        cores = {
            "Produtividade": "#FFD700",  # amarelo
            "Qualidade": "#1E90FF",      # azul
            "Segurança": "#32CD32"       # verde
        }

        # Gráfico
        st.subheader(f"📈 Turno {nome_turno}: Média dos Indicadores por Empilhador")
        fig = px.bar(
            df_melted,
            x="Empilhador",
            y="Porcentagem",
            color="Indicador",
            text="Texto",
            barmode="group",
            title=f"Turno {nome_turno} - Média de Produtividade, Qualidade e Segurança (%)",
            color_discrete_map=cores
        )
        fig.update_traces(textposition="outside", textfont_size=12)
        fig.update_layout(
            yaxis=dict(
                range=[0, 1.1],
                tickvals=[i / 100 for i in range(0, 101, 10)],
                tickformat=".0%"
            ),
            xaxis_tickangle=-45,
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(l=40, r=20, t=60, b=40),
            font=dict(family="Arial", size=13),
            showlegend=True,
            dragmode=False,
            modebar_remove=['zoom', 'pan', 'select', 'lasso', 'zoomIn', 'zoomOut', 'autoScale', 'resetScale'],
            modebar_add=['toImage'],
        )
        st.plotly_chart(fig, use_container_width=True)

        # Tabela formatada
        media_formatada = media_turno.copy()
        for col in indicadores + ["Média Total"]:
            media_formatada[col] = media_formatada[col].apply(
                lambda x: f"{x:.1%}" if pd.notna(x) else "N/A"
            )
        st.dataframe(media_formatada)

    

    # Executa para os dois turnos
    gerar_grafico_por_turno("A", turno_a)
    gerar_grafico_por_turno("B e C", turno_b_c)

else:
    st.info("📎 Envie o arquivo Excel com as colunas: Empilhador, Produtividade, Qualidade e Segurança.")
