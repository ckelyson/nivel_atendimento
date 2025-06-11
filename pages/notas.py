import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Avaliação dos Líderes", layout="wide")
st.title("📊 Avaliação dos Líderes - Notas em %")

uploaded_file = st.file_uploader("📂 Envie o arquivo Excel (.xlsx)", type=["xlsx"])

if uploaded_file:
    # Lê todas as abas disponíveis
    xl = pd.ExcelFile(uploaded_file, engine="openpyxl")
    abas = xl.sheet_names
    aba_selecionada = st.selectbox("🗂️ Selecione a planilha", abas)
    
    # Lê a aba selecionada
    df = xl.parse(aba_selecionada)
    df.columns = df.columns.str.strip()  # Remove espaços extras

    st.subheader("📋 Tabela Original Carregada")
    st.dataframe(df)

    # Verifica se as colunas necessárias existem
    colunas_esperadas = ["Líder de manufatura", "Produtividade", "Segurança", "Qualidade"]
    if all(col in df.columns for col in colunas_esperadas):
        # Agrupa por líder e calcula a média
        notas_media = df.groupby("Líder de manufatura")[["Produtividade", "Segurança", "Qualidade"]].mean()
        notas_media["Total"] = notas_media.mean(axis=1)

        # Converte para porcentagem
        notas_percentual = notas_media / 10
        notas_percentual = notas_percentual.sort_values("Total")  # ordena por Total

        # Gráfico
        st.subheader("📈 Total (%) por Líder")
        df_grafico = notas_percentual.reset_index()
        df_grafico["Total (%)"] = df_grafico["Total"]

        fig = px.bar(
            df_grafico,
            x="Líder de manufatura",
            y="Total (%)",
            text=df_grafico["Total (%)"].map(lambda x: f"{x:.2%}"),
            color="Total (%)",
            color_continuous_scale="Viridis",
        )
        fig.update_traces(textposition="outside", textfont_size=12)
        fig.update_layout(
            yaxis=dict(range=[0, .11], tickformat=".0%"),
            xaxis_tickangle=-45,
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family="Arial", size=13),
            margin=dict(l=40, r=20, t=60, b=40),
            dragmode=False,
            showlegend=False,
            modebar_remove=['zoom', 'pan', 'select', 'lasso', 'zoomIn', 'zoomOut', 'autoScale', 'resetScale'],
            modebar_add=['toImage'],
        )
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("❗ A aba selecionada não contém as colunas: Líder de manufatura, Produtividade, Segurança e Qualidade.")
else:
    st.info("📎 Envie um arquivo Excel com as colunas de notas dos líderes.")

