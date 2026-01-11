# app.py
# Dashboard minimalista (dark) para publicar no Streamlit Community Cloud
# Requisitos: streamlit, pandas, requests, matplotlib

import time
import requests
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


# ----------------------------
# Page config
# ----------------------------
st.set_page_config(
    page_title="Análise de Deputados (Câmara)",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------
# Minimal dark UI polish (CSS)
# ----------------------------
st.markdown(
    """
<style>
/* Layout: menos “gordura” no topo */
.block-container { padding-top: 2rem; padding-bottom: 2.5rem; }

/* Sidebar mais escura e elegante */
section[data-testid="stSidebar"] { background-color: #0B0F14; }

/* Tipografia: títulos com presença */
h1, h2, h3 { font-weight: 650; letter-spacing: -0.02em; }

/* Cards de métricas (KPIs) */
[data-testid="metric-container"] {
    background-color: #161B22;
    padding: 1rem 1rem;
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.06);
}

/* Botões */
.stButton > button {
    border-radius: 10px;
    font-weight: 600;
    padding: 0.55rem 0.85rem;
}

/* Inputs */
[data-baseweb="input"] input, [data-baseweb="select"] > div {
    border-radius: 10px !important;
}

/* Tabelas/Dataframe: leve contorno */
[data-testid="stDataFrame"] {
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px;
    overflow: hidden;
}

/* Divisórias discretas */
hr { border-color: rgba(255,255,255,0.08); }
</style>
""",
    unsafe_allow_html=True,
)

# ----------------------------
# Constants / Helpers
# ----------------------------
BASE_URL = "https://dadosabertos.camara.leg.br/api/v2"


def _safe_int(x, default=0):
    try:
        return int(x)
    except Exception:
        return default


# ----------------------------
# Data loading (session cache)
# - robust for Streamlit reruns
# - avoids hammering the API
# ----------------------------
def fetch_deputados_from_api() -> pd.DataFrame:
    url = f"{BASE_URL}/deputados"
    params = {"itens": 1000, "ordem": "ASC", "ordenarPor": "nome"}

    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    data = r.json().get("dados", [])
    df = pd.DataFrame(data)

    # garante colunas principais
    expected = ["id", "nome", "siglaPartido", "siglaUf", "uri", "uriPartido", "urlFoto"]
    for c in expected:
        if c not in df.columns:
            df[c] = None

    # limpeza mínima
    df["nome"] = df["nome"].astype(str)
    df["siglaPartido"] = df["siglaPartido"].astype(str)
    df["siglaUf"] = df["siglaUf"].astype(str)

    return df


def get_data(ttl_seconds: int, force_refresh: bool) -> tuple[pd.DataFrame, str]:
    """
    Retorna (df, status_text)
    Cache simples em session_state com TTL.
    """
    now = time.time()

    # init cache
    if "cache_df" not in st.session_state:
        st.session_state.cache_df = pd.DataFrame()
        st.session_state.cache_ts = 0.0
        st.session_state.cache_error = None

    expired = (now - st.session_state.cache_ts) > ttl_seconds
    should_refresh = force_refresh or expired or st.session_state.cache_df.empty

    if not should_refresh:
        return st.session_state.cache_df, "cache"

    try:
        df = fetch_deputados_from_api()
        st.session_state.cache_df = df
        st.session_state.cache_ts = now
        st.session_state.cache_error = None
        return df, "api"
    except Exception as e:
        st.session_state.cache_error = str(e)
        # se já tinha cache antigo, devolve ele com aviso
        if not st.session_state.cache_df.empty:
            return st.session_state.cache_df, "cache_stale"
        return pd.DataFrame(), "error"


def apply_filters(df: pd.DataFrame, partidos_sel, ufs_sel, sort_by: str) -> pd.DataFrame:
    out = df.copy()

    if partidos_sel:
        out = out[out["siglaPartido"].isin(partidos_sel)]

    if ufs_sel:
        out = out[out["siglaUf"].isin(ufs_sel)]

    if sort_by in out.columns:
        out = out.sort_values(sort_by, kind="stable")

    return out.reset_index(drop=True)


def counts_table(series: pd.Series, col_name: str) -> pd.DataFrame:
    vc = series.value_counts()
    return pd.DataFrame({col_name: vc.index, "qtdDeputados": vc.values})


# ----------------------------
# Charts (matplotlib)
# ----------------------------
def chart_partidos_bar(df: pd.DataFrame):
    counts = df["siglaPartido"].value_counts().head(20)
    fig, ax = plt.subplots()
    counts.sort_values().plot(kind="barh", ax=ax)
    ax.set_xlabel("Quantidade")
    ax.set_ylabel("Partido")
    ax.set_title("Top 20 partidos")
    fig.tight_layout()
    return fig


def chart_estados_bar(df: pd.DataFrame):
    counts = df["siglaUf"].value_counts()
    fig, ax = plt.subplots()
    counts.sort_values().plot(kind="barh", ax=ax)
    ax.set_xlabel("Quantidade")
    ax.set_ylabel("UF")
    ax.set_title("Deputados por UF")
    fig.tight_layout()
    return fig


def chart_top5_pizza(df: pd.DataFrame):
    counts = df["siglaPartido"].value_counts().head(5)
    fig, ax = plt.subplots()
    ax.pie(counts.values, labels=counts.index, autopct="%1.1f%%", startangle=90)
    ax.set_title("Top 5 partidos (share)")
    fig.tight_layout()
    return fig


# ----------------------------
# UI components
# ----------------------------
def kpi_row(df: pd.DataFrame):
    total = len(df)
    n_partidos = df["siglaPartido"].nunique(dropna=True)
    n_ufs = df["siglaUf"].nunique(dropna=True)

    top_partido = "-"
    top_qtd = "-"
    if total > 0:
        vc = df["siglaPartido"].value_counts()
        if not vc.empty:
            top_partido = vc.index[0]
            top_qtd = _safe_int(vc.iloc[0])

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Deputados", f"{total}")
    c2.metric("Partidos", f"{n_partidos}")
    c3.metric("UFs", f"{n_ufs}")
    c4.metric("Maior partido", f"{top_partido}", delta=f"{top_qtd} deputados" if top_partido != "-" else None)


def download_csv_button(df: pd.DataFrame, filename: str, label: str = "⬇️ Baixar CSV"):
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label=label,
        data=csv,
        file_name=filename,
        mime="text/csv",
        use_container_width=True,
    )


def deputy_details_card(row: dict):
    col1, col2 = st.columns([1, 2])

    with col1:
        foto = row.get("urlFoto")
        if foto and foto != "None":
            st.image(foto, use_container_width=True)
        else:
            st.info("Sem foto disponível.")

    with col2:
        st.markdown(f"### {row.get('nome', '-')}")
        st.write(f"**Partido:** {row.get('siglaPartido', '-')}")
        st.write(f"**UF:** {row.get('siglaUf', '-')}")
        uri = row.get("uri")
        if uri and uri != "None":
            st.link_button("🔗 Abrir referência (uri)", uri)


# ----------------------------
# Header
# ----------------------------
st.markdown("## 🏛️ Análise de Deputados Federais")
st.caption("Dashboard minimalista (dark) com filtros, gráficos e exportação.")

# ----------------------------
# Sidebar (minimal + UX)
# ----------------------------
with st.sidebar:
    st.markdown("## ⚙️ Controles")

    # cache/refresh controls
    ttl_minutes = st.number_input(
        "Cache (min)",
        min_value=5,
        max_value=720,
        value=60,
        step=5,
        help="Evita bater na API a cada atualização. Ideal para Cloud.",
    )
    ttl_seconds = int(ttl_minutes * 60)

    col_a, col_b = st.columns(2)
    with col_a:
        refresh = st.button("🔄 Atualizar", use_container_width=True)
    with col_b:
        clear = st.button("🧹 Limpar", use_container_width=True)

    if clear:
        st.session_state.cache_df = pd.DataFrame()
        st.session_state.cache_ts = 0.0
        st.session_state.cache_error = None
        st.toast("Cache limpo ✅", icon="✅")

    st.divider()
    st.markdown("### 🔎 Filtros")

# ----------------------------
# Load data
# ----------------------------
df, source = get_data(ttl_seconds=ttl_seconds, force_refresh=refresh)

if df.empty:
    err = st.session_state.get("cache_error")
    st.error("Não foi possível carregar os dados agora.")
    if err:
        st.caption(f"Detalhe técnico: {err}")
    st.stop()

# ----------------------------
# Filters (dynamic)
# ----------------------------
all_partidos = sorted(df["siglaPartido"].dropna().unique().tolist())
all_ufs = sorted(df["siglaUf"].dropna().unique().tolist())

with st.sidebar:
    partidos_sel = st.multiselect("Partidos", all_partidos, default=[])
    ufs_sel = st.multiselect("UFs", all_ufs, default=[])

    st.divider()
    st.markdown("### 📊 Exibição")
    sort_by = st.selectbox("Ordenar por", ["nome", "siglaPartido", "siglaUf"], index=0)
    page_size = st.selectbox("Linhas na tabela", [25, 50, 100, 200], index=1)

    st.divider()
    if source == "api":
        st.caption("Dados atualizados via API agora.")
    elif source == "cache":
        st.caption("Dados do cache.")
    elif source == "cache_stale":
        st.caption("Cache (API indisponível no momento).")
    st.caption("Fonte: Dados Abertos da Câmara")

df_f = apply_filters(df, partidos_sel=partidos_sel, ufs_sel=ufs_sel, sort_by=sort_by)

# ----------------------------
# Tabs
# ----------------------------
tabs = st.tabs(["📌 Visão geral", "🏷️ Partidos", "🗺️ Estados", "👥 Deputados", "ℹ️ Sobre"])

# --- Tab 1: Visão geral ---
with tabs[0]:
    kpi_row(df_f)
    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Deputados por partido")
        st.pyplot(chart_partidos_bar(df_f), clear_figure=True)

    with col2:
        st.markdown("### Deputados por UF")
        st.pyplot(chart_estados_bar(df_f), clear_figure=True)

    st.markdown("### Top 5 partidos")
    st.pyplot(chart_top5_pizza(df_f), clear_figure=True)

    st.divider()
    download_csv_button(df_f, "deputados_filtrados.csv")

# --- Tab 2: Partidos ---
with tabs[1]:
    st.markdown("### Ranking de partidos")
    cont_partidos = counts_table(df_f["siglaPartido"], "siglaPartido")
    st.dataframe(cont_partidos, use_container_width=True, hide_index=True)

    st.divider()
    download_csv_button(cont_partidos, "contagem_partidos.csv")

# --- Tab 3: Estados ---
with tabs[2]:
    st.markdown("### Ranking por UF")
    cont_ufs = counts_table(df_f["siglaUf"], "siglaUf")
    st.dataframe(cont_ufs, use_container_width=True, hide_index=True)

    st.divider()
    download_csv_button(cont_ufs, "contagem_estados.csv")

# --- Tab 4: Deputados ---
with tabs[3]:
    st.markdown("### Explorar deputados")
    search = st.text_input("Buscar por nome", value="", placeholder="Digite um nome…")

    df_view = df_f.copy()
    if search.strip():
        df_view = df_view[df_view["nome"].str.contains(search, case=False, na=False)]

    st.dataframe(df_view.head(page_size), use_container_width=True, hide_index=True)

    st.divider()

    st.markdown("### Detalhe rápido")
    options = df_view["nome"].dropna().unique().tolist()
    selected = st.selectbox("Selecione um deputado", [""] + options)

    if selected:
        row = df_view[df_view["nome"] == selected].iloc[0].to_dict()
        deputy_details_card(row)

    st.divider()
    download_csv_button(df_view, "deputados_explorados.csv")

# --- Tab 5: Sobre ---
with tabs[4]:
    st.markdown(
        """
### Sobre

Dashboard interativa para analisar a composição atual da Câmara dos Deputados,
com foco em **distribuição por partido**, **distribuição por UF** e **Top 5 partidos**.

**Stack:** Python · Pandas · Streamlit · Matplotlib  
**Fonte:** API de Dados Abertos da Câmara dos Deputados  
"""
    )
    st.info("Dica: ajuste o tempo de cache na barra lateral para melhor performance na Cloud.")
