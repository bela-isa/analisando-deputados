import streamlit as st
import pandas as pd

from src.data import fetch_deputados_df, apply_filters
from src.charts import chart_partidos_bar, chart_estados_bar, chart_top5_pizza
from src.ui import kpi_row, download_section, deputy_details_card

st.set_page_config(
    page_title="Análise de Deputados (Câmara)",
    page_icon="🏛️",
    layout="wide",
)

st.title("🏛️ Análise de Deputados Federais (Brasil)")
st.caption("Dashboard interativa usando a API de Dados Abertos da Câmara dos Deputados.")

with st.sidebar:
    st.header("⚙️ Controles")

    ttl_minutes = st.number_input("Cache (min)", min_value=5, max_value=720, value=60, step=5)
    ttl_seconds = int(ttl_minutes * 60)

    col_a, col_b = st.columns(2)
    with col_a:
        refresh = st.button("🔄 Atualizar dados", use_container_width=True)
    with col_b:
        clear_cache = st.button("🧹 Limpar cache", use_container_width=True)

    if clear_cache:
        fetch_deputados_df.clear()
        st.toast("Cache limpo ✅", icon="✅")

    st.divider()
    st.subheader("🔎 Filtros")

df = fetch_deputados_df(ttl_seconds=ttl_seconds, force_refresh=refresh)

if df.empty:
    st.error("Não foi possível carregar os dados agora. Tente novamente.")
    st.stop()

# filtros dinâmicos
all_partidos = sorted(df["siglaPartido"].dropna().unique().tolist())
all_ufs = sorted(df["siglaUf"].dropna().unique().tolist())

with st.sidebar:
    partidos_sel = st.multiselect("Partidos", all_partidos, default=[])
    ufs_sel = st.multiselect("UFs", all_ufs, default=[])
    sort_by = st.selectbox("Ordenar por", ["nome", "siglaPartido", "siglaUf"], index=0)
    page_size = st.selectbox("Linhas na tabela", [25, 50, 100, 200], index=1)

df_f = apply_filters(df, partidos_sel=partidos_sel, ufs_sel=ufs_sel, sort_by=sort_by)

tabs = st.tabs(["📌 Visão geral", "🏷️ Partidos", "🗺️ Estados", "👥 Deputados", "ℹ️ Sobre"])

# -------------------- Visão geral --------------------
with tabs[0]:
    kpi_row(df_f)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Deputados por partido")
        st.pyplot(chart_partidos_bar(df_f), clear_figure=True)

    with col2:
        st.subheader("Deputados por UF")
        st.pyplot(chart_estados_bar(df_f), clear_figure=True)

    st.subheader("Top 5 partidos (pizza)")
    st.pyplot(chart_top5_pizza(df_f), clear_figure=True)

    download_section(df_f, label_prefix="visao_geral")

# -------------------- Partidos --------------------
with tabs[1]:
    st.subheader("Ranking de partidos")
    cont_partidos = df_f["siglaPartido"].value_counts().reset_index()
    cont_partidos.columns = ["siglaPartido", "qtdDeputados"]
    st.dataframe(cont_partidos, use_container_width=True)

    download_section(cont_partidos, label_prefix="partidos")

# -------------------- Estados --------------------
with tabs[2]:
    st.subheader("Ranking por UF")
    cont_ufs = df_f["siglaUf"].value_counts().reset_index()
    cont_ufs.columns = ["siglaUf", "qtdDeputados"]
    st.dataframe(cont_ufs, use_container_width=True)

    download_section(cont_ufs, label_prefix="estados")

# -------------------- Deputados --------------------
with tabs[3]:
    st.subheader("Explorar deputados")
    search = st.text_input("Buscar por nome", value="")
    df_view = df_f.copy()

    if search.strip():
        df_view = df_view[df_view["nome"].str.contains(search, case=False, na=False)]

    st.dataframe(
        df_view.head(page_size),
        use_container_width=True,
        hide_index=True
    )

    st.markdown("### Detalhe rápido")
    selected_name = st.selectbox(
        "Selecione um deputado (pela lista filtrada)",
        options=[""] + df_view["nome"].dropna().unique().tolist()
    )

    if selected_name:
        row = df_view[df_view["nome"] == selected_name].iloc[0].to_dict()
        deputy_details_card(row)

    download_section(df_view, label_prefix="deputados")

# -------------------- Sobre --------------------
with tabs[4]:
    st.subheader("Sobre o projeto")
    st.write(
        """
Este app é uma interface do projeto **Análise de Dados: Deputados Federais**,
que analisa a distribuição por **partido**, **estado** e o **top 5 partidos**.
"""
    )
    st.markdown("- Fonte: API de Dados Abertos da Câmara dos Deputados.")
    st.info("Dica: use cache para não bater na API a cada rerun.")
