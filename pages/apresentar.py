import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Distribuição de Notas (7 a 10)", layout="wide")
st.title("📊 Distribuição de Notas (7 a 10)")

uploaded_file = st.file_uploader("📂 Envie o arquivo Excel (.xlsx)", type=["xlsx"])

if uploaded_file:
    # Lê todas as abas disponíveis
    xl = pd.ExcelFile(uploaded_file, engine="openpyxl")
    abas = xl.sheet_names
    aba_selecionada = st.selectbox("🗂️ Selecione a planilha", abas)

    # Lê a aba selecionada
    df = xl.parse(aba_selecionada)
    df.columns = df.columns.str.strip()

    # Define os blocos de perguntas
    perguntas_produtividade = ["Atendimento a Produção", "Proatividade (Facilitador)", "Demanda fora de rotina"]
    perguntas_seguranca = ["EPIs", "Contribui para Segurança", "Conduta de Segurança"]
    perguntas_qualidade = ["5S", "Atendimento Rádio", "Expectativa"]

    perguntas_nota = perguntas_produtividade + perguntas_seguranca + perguntas_qualidade

    # Função para contar e calcular porcentagens de 7 a 10
    def contar_notas(colunas):
        notas = df[colunas].round(0).astype(int).values.flatten()
        serie = pd.Series(notas)
        serie_filtrada = serie[serie >= 7]  # mantém só de 7 a 10
        contagem = serie_filtrada.value_counts().reindex([10, 9, 8, 7], fill_value=0)
        total = contagem.sum()
        return pd.DataFrame({
            "Nota": contagem.index.astype(str),
            "Porcentagem": (contagem.values / total) * 100
        })

    # Colunas com gráficos separados
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 🔵 Produtividade")
        dados_prod = contar_notas(perguntas_produtividade)
        fig_prod = px.pie(
            dados_prod,
            names="Nota",
            values="Porcentagem",
            title="Notas de Produtividade (7 a 10)",
            hole=0.3
        )
        fig_prod.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_prod, use_container_width=True)

    with col2:
        st.markdown("### 🟡 Segurança")
        dados_seg = contar_notas(perguntas_seguranca)
        fig_seg = px.pie(
            dados_seg,
            names="Nota",
            values="Porcentagem",
            title="Notas de Segurança (7 a 10)",
            hole=0.3
        )
        fig_seg.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_seg, use_container_width=True)

    with col3:
        st.markdown("### 🟢 Qualidade")
        dados_qual = contar_notas(perguntas_qualidade)
        fig_qual = px.pie(
            dados_qual,
            names="Nota",
            values="Porcentagem",
            title="Notas de Qualidade (7 a 10)",
            hole=0.3
        )
        fig_qual.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_qual, use_container_width=True)

    # 🎯 Gráfico de distribuição geral de 7 a 10
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
    fig_geral.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_geral, use_container_width=True)

else:
    st.info("📎 Envie um arquivo Excel com 9 colunas de perguntas com notas de 0 a 10.")

