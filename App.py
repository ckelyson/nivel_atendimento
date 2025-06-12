import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Média Geral por Turno", layout="wide")
st.title("📊 Média Geral de Indicadores por Turno")

uploaded_file = st.file_uploader("📂 Envie o arquivo Excel (.xlsx)", type=["xlsx"])

if uploaded_file:
    xl = pd.ExcelFile(uploaded_file, engine='openpyxl')
    abas = xl.sheet_names
    aba_selecionada = st.selectbox("🗂️ Selecione a planilha", abas)
    
    df = xl.parse(aba_selecionada)
    df.columns = df.columns.str.strip()

    df = df.rename(columns={
        "Líder de manufatura": "Líder",
        "Empilhador:": "Empilhador"
    })

    # Indicadores desejados
    indicadores = ["Produtividade", "Qualidade", "Segurança"]

    # Formata colunas finais como porcentagens (como decimal)
    colunas_para_formatar = indicadores + ["Total"]
    for coluna in colunas_para_formatar:
        df[coluna] = df[coluna].astype(str).str.replace('%', '').str.replace(',', '.').astype(float) / 1

    st.subheader("📋 Tabela ")
    st.dataframe(df)

    # Listas dos empilhadores por turno
    turno_a = ["Alison", "Aucimar", "Adilson", "Andre", "Fabiano"]
    turno_b_c = ["Edivan", "Ezequias", "Genivaldo", "João Gomes", "João Vitor", "Leandro", "Obério", "Jhone Kened"]

    # Função para formatar percentuais
    def formatar_percentual(valor):
        return f"{valor:.2%}".replace(".", ",")

    # Calcula médias
    media_total_geral = df["Total"].mean()
    media_turno_a = df[df["Empilhador"].isin(turno_a)]["Total"].mean()
    media_turno_b_c = df[df["Empilhador"].isin(turno_b_c)]["Total"].mean()

    # Exibe médias
    st.success(f"📌 **Média Geral Total**: **{formatar_percentual(media_total_geral)}**")
    st.success(f"📌 **Média Geral do Turno A**: **{formatar_percentual(media_turno_a)}**")
    st.success(f"📌 **Média Geral do Turno B e C**: **{formatar_percentual(media_turno_b_c)}**")

    # Prepara DataFrame para gráfico
    medias_turnos = pd.DataFrame({
        "Turno": ["A", "B e C", "Geral"],
        "Média Total": [media_turno_a, media_turno_b_c, media_total_geral]
    })
    medias_turnos["Texto"] = medias_turnos["Média Total"].apply(formatar_percentual)

    # Gráfico de barras
    st.subheader("📊 Gráfico Comparativo das Médias Gerais por Turno")
    fig = px.bar(
        medias_turnos,
        x="Turno",
        y="Média Total",
        text="Texto",
        color="Turno",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig.update_traces(textposition="outside", textfont_size=14)
    fig.update_layout(
        yaxis=dict(range=[0, 1.1], tickformat=".0%"),
        title="Média Geral da Coluna 'Total' por Turno",
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Arial", size=13)
    )
    st.plotly_chart(fig, use_container_width=True)

    

else:
    st.info("📎 Envie o arquivo Excel com as colunas: Empilhador, Produtividade, Qualidade, Segurança e Total.")
