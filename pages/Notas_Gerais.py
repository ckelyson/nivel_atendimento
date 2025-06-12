import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Distribuição de Notas (7 a 10)", layout="wide")
st.title("📊 Distribuição de Notas (7 a 10)")

uploaded_file = st.file_uploader("📂 Envie o arquivo Excel (.xlsx)", type=["xlsx"])

if uploaded_file:
    xl = pd.ExcelFile(uploaded_file, engine="openpyxl")
    abas = xl.sheet_names
    aba_selecionada = st.selectbox("🗂️ Selecione a planilha", abas)

    df = xl.parse(aba_selecionada)
    df.columns = df.columns.str.strip()

    perguntas_produtividade = ["Atendimento a Produção", "Proatividade (Facilitador)", "Demanda fora de rotina"]
    perguntas_seguranca = ["EPIs", "Contribui para Segurança", "Conduta de Segurança"]
    perguntas_qualidade = ["5S", "Atendimento Rádio", "Expectativa"]

    perguntas_nota = perguntas_produtividade + perguntas_seguranca + perguntas_qualidade

    # Mapeamento de cores por nota
    cores_notas = {
        "10": "#2ecc71",  # verde
        "9": "#3498db",   # azul
        "8": "#f1c40f",   # amarelo
        "7": "#e67e22"    # laranja
    }

    def contar_notas(colunas):
        notas = df[colunas].round(0).astype(int).values.flatten()
        serie = pd.Series(notas)
        serie_filtrada = serie[serie >= 7]
        contagem = serie_filtrada.value_counts().reindex([10, 9, 8, 7], fill_value=0)
        return pd.DataFrame({
            "Nota": contagem.index.astype(str),
            "Porcentagem": (contagem.values / contagem.sum()) * 100
        })

    def gerar_grafico(dados, titulo):
        fig = px.pie(
            dados,
            names="Nota",
            values="Porcentagem",
            title=titulo,
            hole=0.3
        )
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            marker=dict(colors=[cores_notas[n] for n in dados["Nota"]])
        )
        return fig

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 🔵 Produtividade")
        dados_prod = contar_notas(perguntas_produtividade)
        st.plotly_chart(gerar_grafico(dados_prod, "Notas de Produtividade (7 a 10)"), use_container_width=True)

    with col2:
        st.markdown("### 🟡 Segurança")
        dados_seg = contar_notas(perguntas_seguranca)
        st.plotly_chart(gerar_grafico(dados_seg, "Notas de Segurança (7 a 10)"), use_container_width=True)

    with col3:
        st.markdown("### 🟢 Qualidade")
        dados_qual = contar_notas(perguntas_qualidade)
        st.plotly_chart(gerar_grafico(dados_qual, "Notas de Qualidade (7 a 10)"), use_container_width=True)

    # Distribuição geral
    st.markdown("### 🎯 Distribuição Geral das Notas (7 a 10)")
    todas_as_notas = df[perguntas_nota].round(0).astype(int).values.flatten()
    serie_notas = pd.Series(todas_as_notas)
    serie_filtrada = serie_notas[serie_notas >= 7]
    frequencia_notas = serie_filtrada.value_counts().reindex([10, 9, 8, 7], fill_value=0)

    df_freq = pd.DataFrame({
        "Nota": frequencia_notas.index.astype(str),
        "Frequência": frequencia_notas.values
    })

    fig_geral = px.pie(
        df_freq,
        names="Nota",
        values="Frequência",
        title="Distribuição Geral das Notas (7 a 10)",
        hole=0.3
    )
    fig_geral.update_traces(
        textposition='inside',
        textinfo='percent+label',
        marker=dict(colors=[cores_notas[n] for n in df_freq["Nota"]])
    )
    st.plotly_chart(fig_geral, use_container_width=True)

else:
    st.info("📎 Envie um arquivo Excel com 9 colunas de perguntas com notas de 0 a 10.")
