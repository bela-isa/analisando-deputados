# app.py
# Futuristic / minimal (dark) Streamlit dashboard with subtle neon accents
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
    page_title="Análise de Deputados Federais",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ----------------------------
# Futuristic minimal UI (CSS)
# ----------------------------
st.markdown(
    """
<style>
:root{
  --bg: #0B0F14;
  --panel: #0E141B;
  --panel2:#101824;
  --text: #E6EDF3;
  --muted:#9AA6B2;
  --border: rgba(255,255,255,0.07);
  --neon: #39FFB6;         /* neon mint */
  --neon2:#5D5BFF;         /* neon violet */
  --neon3:#4F8EF7;         /* electric blue */
}

/* Overall padding */
.block-container { padding-top: 2rem; padding-bottom: 2.5rem; }

/* Sidebar */
section[data-testid="stSidebar"]{
  background: linear-gradient(180deg, #070A0F 0%, var(--bg) 65%);
  border-right: 1px solid var(--border);
}

/* Headings */
h1, h2, h3{
  font-weight: 700;
  letter-spacing: -0.03em;
}
p, label, span { color: var(--text); }

/* Subtle neon underline for main title */
.title-neon{
  display: inline-block;
  padding-bottom: .35rem;
  border-bottom: 1px solid rgba(57,255,182,0.35);
  box-shadow: 0 14px 32px rgba(57,255,182,0.06);
}

/* Metric cards */
[data-testid="metric-container"]{
  background: radial-gradient(1200px 160px at 10% 0%, rgba(93,91,255,0.12), rgba(0,0,0,0) 55%),
              linear-gradient(180deg, var(--panel) 0%, #0B1017 100%);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 1rem 1rem;
}
[data-testid="metric-container"] div{
  color: var(--text);
}

/* Buttons */
.stButton > button{
  border-radius: 12px;
  font-weight: 650;
  padding: 0.60rem 0.90rem;
  border: 1px solid rgba(79,142,247,0.25);
  background: linear-gradient(180deg, rgba(79,142,247,0.12) 0%, rgba(79,142,247,0.04) 100%);
}
.stButton > button:hover{
  border-color: rgba(57,255,182,0.35);
  box-shadow: 0 10px 28px rgba(57,255,182,0.10);
}

/* Inputs */
[data-baseweb="select"] > div, [data-baseweb="input"] input{
  border-radius: 12px !important;
  border-color: rgba(255,255,255,0.10) !important;
  background-color: rgba(16,24,36,0.55) !important;
}

/* Dataframe */
[data-testid="stDataFrame"]{
  border: 1px solid var(--border);
  border-radius: 16px;
  overflow: hidden;
}

/* Dividers */
hr{ border-color: rgba(255,255,255,0.08); }

/* Tabs - more futuristic */
button[data-baseweb="tab"]{
  font-weight: 650;
  color: var(--muted);
}
button[data-baseweb="tab"][aria-selected="true"]{
  color: var(--text);
  border-bottom: 2px solid rgba(57,255,182,0.8) !important;
}

/* Links / link buttons */
a, a:visited { color: rgba(57,255,182,0.9); }
</style>
""",
    unsafe_allow_html=True,
)


# ----------------------------
# Constants / Helpers
# ----------------------------
BASE_URL = "https://dadosabertos.camara.leg.br/api/v2"


def _fmt_int(n: int) -> str:
    return f"{int(n):,}".replace(",", ".")


def _safe_int(x, default=0):
    try:
        return int(x)
    except Exception:
        return default


# ----------------------------
# Data loading (session cache w/ TTL)
# ----------------------------
def fetch_deputados_from_api() -> pd.DataFrame:
    url = f"{BASE_URL}/deputados"
    params = {"itens": 1000, "ordem": "ASC", "ordenarPor": "nome"}

    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    data = r.json().get("dados", [])
    df = pd.DataFrame(data)

    # Ensure expected columns exist
    expected = ["id", "nome", "siglaPartido", "siglaUf", "uri", "uriPartido", "urlFoto"]
    for c in expected:
        if c not in df.columns:
            df[c] = None

    # Normalize types
    df["nome"] = df["nome"].astype(str)
    df["siglaPartido"] = df["siglaPartido"].astype(str)
    df["siglaUf"] = df["siglaUf"].astype(str)

    return df


def get_data(ttl_seconds: int, force_refresh: bool) -> tuple[pd.DataFrame, str]:
    """
    Returns (df, status)
    status: 'api' | 'cache' | 'cache_stale' | 'error'
    """
    now = time.time()

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
# Charts (matplotlib) - dark integrated, subtle neon
# ----------------------------
def _style_dark_axes(ax):
    fg = "#E6EDF3"
    muted = "#9AA6B2"
    panel = "#0E141B"
    grid = (1, 1, 1, 0.08)

    ax.set_facecolor(panel)
    ax.tick_params(colors=muted)
    for spine in ax.spines.values():
        spine.set_color((1, 1, 1, 0.10))
    ax.xaxis.label.set_color(muted)
    ax.yaxis.label.set_color(muted)
    ax.title.set_color(fg)
    ax.grid(True, axis="x", color=grid, linewidth=1)
    ax.set_axisbelow(True)


def chart_partidos_bar(df: pd.DataFrame):
    counts = df["siglaPartido"].value_counts().head(20).sort_values()

    fig, ax = plt.subplots()
    fig.patch.set_facecolor("#0B0F14")
    _style_dark_axes(ax)

    # Subtle neon edge: bar with low alpha fill + neon edge
    bars = ax.barh(counts.index, counts.values)
    for b in bars:
        b.set_alpha(0.18)
        b.set_edgecolor((57/255, 1.0, 182/255, 0.70))
        b.set_linewidth(1.2)

    ax.set_xlabel("Quantidade")
    ax.set_ylabel("")
    ax.set_title("Deputados por partido (Top 20)")
    fig.tight_layout()
    return fig


def chart_estados_bar(df: pd.DataFrame):
    counts = df["siglaUf"].value_counts().sort_values()

    fig, ax = plt.subplots()
    fig.patch.set_facecolor("#0B0F14")
    _style_dark_axes(ax)

    bars = ax.barh(counts.index, counts.values)
    for b in bars:
        b.set_alpha(0.18)
        b.set_edgecolor((79/255, 142/255, 247/255, 0.70))
        b.set_linewidth(1.2)

    ax.set_xlabel("Quantidade")
    ax.set_ylabel("")
    ax.set_title("Deputados por UF")
    fig.tight_layout()
    return fig


def chart_top5_pizza(df: pd.DataFrame):
    counts = df["siglaPartido"].value_counts().head(5)

    fig, ax = plt.subplots()
    fig.patch.set_facecolor("#0B0F14")
    ax.set_facecolor("#0E141B")

    # Keep it subtle: no loud colors; dark wedges with neon edge
    wedges, texts, autotexts = ax.pie(
        counts.values,
        labels=counts.index,
        autopct="%1.1f%%",
        startangle=90,
        textprops={"color": "#E6EDF3"},
    )
    for w in wedges:
        w.set_alpha(0.25)
        w.set_edgecolor((93/255, 91/255, 1.0, 0.65))
        w.set_linewidth(1.2)

    for t in autotexts:
        t.set_color("#E6EDF3")
        t.set_fontweight("600")

    ax.set_title("Participação do Top 5 partidos")
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
    top_qtd = 0
    if total > 0:
        vc = df["siglaPartido"].value_counts()
        if not vc.empty:
            top_partido = vc.index[0]
            top_qtd = _safe_int(vc.iloc[0])

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Deputados", _fmt_int(total))
    c2.metric("Partidos", _fmt_int(n_partidos))
    c3.metric("UFs", _fmt_int(n_ufs))
    c4.metric("Maior partido", f"{top_partido}", delta=f"{_fmt_int(top_qtd)} deputados" if top_partido != "-" else None)


def download_csv_button(df: pd.DataFrame, filename: str, label: str = "Baixar CSV"):
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
        if foto and str(foto) != "None":
            st.image(foto, use_container_width=True)
        else:
            st.info("Foto indisponível")

    with col2:
        st.markdown(f"#### {row.get('nome', '-')}")
        st.write(f"Partido: **{row.get('siglaPartido', '-')}**")
        st.write(f"UF: **{row.get('siglaUf', '-')}**")
        uri = row.get("uri")
        if uri and str(uri) != "None":
            st.link_button("Abrir referência", uri)


# ----------------------------
# Header (minimal, futuristic)
# ----------------------------
st.markdown('<h1 class="title-neon">Análise de Deputados Federais</h1>', unsafe_allow_html=True)
st.caption("Dashboard interativa para explorar a composição atual da Câmara: partidos, UFs e distribuição proporcional.")


# ----------------------------
# Sidebar (minimal, no emojis)
# ----------------------------
with st.sidebar:
    st.markdown("## Controles")

    ttl_minutes = st.number_input(
        "Cache (min)",
        min_value=5,
        max_value=720,
        value=60,
        step=5,
        help="Reduz chamadas repetidas à API (ideal para deploy na cloud).",
    )
    ttl_seconds = int(ttl_minutes * 60)

    col_a, col_b = st.columns(2)
    with col_a:
        refresh = st.button("Atualizar", use_container_width=True)
    with col_b:
        clear = st.button("Limpar", use_container_width=True)

    if clear:
        st.session_state.cache_df = pd.DataFrame()
        st.session_state.cache_ts = 0.0
        st.session_state.cache_error = None
        st.toast("Cache limpo", icon="✅")

    st.divider()
    st.markdown("## Filtros")


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
    st.markdown("## Exibição")
    sort_by = st.selectbox("Ordenar por", ["nome", "siglaPartido", "siglaUf"], index=0)
    page_size = st.selectbox("Linhas na tabela", [25, 50, 100, 200], index=1)

    st.divider()
    if source == "api":
        st.caption("Dados atualizados agora")
    elif source == "cache":
        st.caption("Dados do cache")
    elif source == "cache_stale":
        st.caption("Cache ativo (API indisponível no momento)")
    st.caption("Fonte: Dados Abertos da Câmara")


df_f = apply_filters(df, partidos_sel=partidos_sel, ufs_sel=ufs_sel, sort_by=sort_by)


# ----------------------------
# Tabs (minimal labels)
# ----------------------------
tabs = st.tabs(["Visão geral", "Partidos", "Estados", "Deputados", "Sobre"])


# --- Tab 1: Visão geral ---
with tabs[0]:
    kpi_row(df_f)
    st.divider()

    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown("### Deputados por partido")
        st.pyplot(chart_partidos_bar(df_f), clear_figure=True)

    with col2:
        st.markdown("### Deputados por UF")
        st.pyplot(chart_estados_bar(df_f), clear_figure=True)

    # "Secret but robust": advanced view inside expander (clean UI, power-user option)
    with st.expander("Análises avançadas", expanded=False):
        st.markdown("### Participação do Top 5 partidos")
        st.pyplot(chart_top5_pizza(df_f), clear_figure=True)

        st.markdown("#### Exportação")
        download_csv_button(df_f, "deputados_filtrados.csv", label="Baixar CSV (filtros atuais)")

    # Quick download (still available, but understated)
    st.divider()
    download_csv_button(df_f, "deputados_filtrados.csv", label="Baixar CSV")


# --- Tab 2: Partidos ---
with tabs[1]:
    st.markdown("### Ranking de partidos")
    cont_partidos = counts_table(df_f["siglaPartido"], "siglaPartido")
    st.dataframe(cont_partidos, use_container_width=True, hide_index=True)

    st.divider()
    download_csv_button(cont_partidos, "contagem_partidos.csv", label="Baixar CSV")


# --- Tab 3: Estados ---
with tabs[2]:
    st.markdown("### Ranking por UF")
    cont_ufs = counts_table(df_f["siglaUf"], "siglaUf")
    st.dataframe(cont_ufs, use_container_width=True, hide_index=True)

    st.divider()
    download_csv_button(cont_ufs, "contagem_estados.csv", label="Baixar CSV")


# --- Tab 4: Deputados ---
with tabs[3]:
    st.markdown("### Explorar deputados")
    search = st.text_input("Buscar por nome", value="", placeholder="Digite um nome...")

    df_view = df_f.copy()
    if search.strip():
        df_view = df_view[df_view["nome"].str.contains(search, case=False, na=False)]

    st.dataframe(df_view.head(page_size), use_container_width=True, hide_index=True)

    st.divider()
    st.markdown("### Detalhes")
    options = df_view["nome"].dropna().unique().tolist()
    selected = st.selectbox("Selecionar deputado", [""] + options)

    if selected:
        row = df_view[df_view["nome"] == selected].iloc[0].to_dict()
        deputy_details_card(row)

    st.divider()
    download_csv_button(df_view, "deputados_explorados.csv", label="Baixar CSV")


# --- Tab 5: Sobre ---
with tabs[4]:
    st.markdown(
        """
### Sobre

Interface para análise da composição atual da Câmara dos Deputados, com foco em:
- distribuição por partido
- distribuição por UF
- filtros e exportação

Stack: Python · Pandas · Streamlit · Matplotlib  
Fonte: API de Dados Abertos da Câmara dos Deputados
"""
    )
    st.info("Sugestão: mantenha cache entre 30 e 120 min para melhor performance na cloud.")
