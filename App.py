# app.py
# Enhanced Streamlit dashboard with improved UX and visual refinements
# Requisitos: streamlit, pandas, requests, matplotlib

import time
import requests
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime

# ----------------------------
# Page config
# ----------------------------
st.set_page_config(
    page_title="Análise de Deputados Federais",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------
# Enhanced futuristic UI (CSS)
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
  --neon: #39FFB6;
  --neon2:#5D5BFF;
  --neon3:#4F8EF7;
  --accent: #FF6B9D;
}

.block-container { 
  padding-top: 1.5rem; 
  padding-bottom: 2.5rem;
  max-width: 1400px;
}

/* Sidebar enhancements */
section[data-testid="stSidebar"]{
  background: linear-gradient(180deg, #070A0F 0%, var(--bg) 65%);
  border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2 {
  font-size: 0.95rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--neon);
  margin-top: 1.5rem;
  margin-bottom: 0.8rem;
}

/* Headings */
h1, h2, h3{
  font-weight: 700;
  letter-spacing: -0.03em;
}
h3 { 
  font-size: 1.3rem;
  margin-bottom: 1rem;
  background: linear-gradient(135deg, var(--text) 0%, var(--muted) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
p, label, span { color: var(--text); }

/* Enhanced title with animated gradient */
.title-neon{
  display: inline-block;
  padding-bottom: .4rem;
  border-bottom: 2px solid;
  border-image: linear-gradient(90deg, var(--neon) 0%, var(--neon3) 50%, var(--accent) 100%) 1;
  box-shadow: 0 18px 38px rgba(57,255,182,0.12);
  animation: glow 3s ease-in-out infinite;
}

@keyframes glow {
  0%, 100% { filter: drop-shadow(0 0 8px rgba(57,255,182,0.4)); }
  50% { filter: drop-shadow(0 0 16px rgba(57,255,182,0.6)); }
}

/* Enhanced metric cards with hover effect */
[data-testid="metric-container"]{
  background: radial-gradient(1200px 160px at 10% 0%, rgba(93,91,255,0.16), rgba(0,0,0,0) 55%),
              linear-gradient(180deg, var(--panel) 0%, #0B1017 100%);
  border: 1px solid rgba(255,255,255,0.10);
  border-radius: 18px;
  padding: 1.2rem 1rem;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

[data-testid="metric-container"]::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(57,255,182,0.08), transparent);
  transition: left 0.5s;
}

[data-testid="metric-container"]:hover::before {
  left: 100%;
}

[data-testid="metric-container"]:hover{
  border-color: rgba(57,255,182,0.30);
  transform: translateY(-2px);
  box-shadow: 0 12px 32px rgba(57,255,182,0.15);
}

[data-testid="stMetricValue"] {
  font-size: 2rem !important;
  font-weight: 800 !important;
}

/* Enhanced buttons with better feedback */
.stButton > button{
  border-radius: 12px;
  font-weight: 650;
  padding: 0.65rem 1.2rem;
  border: 1px solid rgba(79,142,247,0.32);
  background: linear-gradient(180deg, rgba(79,142,247,0.16) 0%, rgba(79,142,247,0.06) 100%);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.stButton > button::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: rgba(57,255,182,0.3);
  transform: translate(-50%, -50%);
  transition: width 0.6s, height 0.6s;
}

.stButton > button:hover::before {
  width: 300px;
  height: 300px;
}

.stButton > button:hover{
  border-color: rgba(57,255,182,0.50);
  box-shadow: 0 12px 32px rgba(57,255,182,0.18);
  transform: translateY(-1px);
}

.stButton > button:active {
  transform: translateY(0px);
}

/* Enhanced inputs */
[data-baseweb="select"] > div, 
[data-baseweb="input"] input,
.stTextInput input{
  border-radius: 12px !important;
  border-color: rgba(255,255,255,0.14) !important;
  background-color: rgba(16,24,36,0.65) !important;
  transition: all 0.3s ease !important;
}

[data-baseweb="select"] > div:hover,
[data-baseweb="input"] input:hover,
.stTextInput input:hover{
  border-color: rgba(57,255,182,0.35) !important;
  box-shadow: 0 0 0 1px rgba(57,255,182,0.15) !important;
}

[data-baseweb="select"] > div:focus-within,
[data-baseweb="input"] input:focus,
.stTextInput input:focus{
  border-color: rgba(57,255,182,0.55) !important;
  box-shadow: 0 0 0 2px rgba(57,255,182,0.20) !important;
}

/* Enhanced dataframe */
[data-testid="stDataFrame"]{
  border: 1px solid rgba(255,255,255,0.10);
  border-radius: 18px;
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}

[data-testid="stDataFrame"] thead tr th {
  background: linear-gradient(180deg, rgba(93, 91, 255, 0.18) 0%, rgba(93, 91, 255, 0.10) 100%) !important;
  color: #E6EDF3 !important;
  font-weight: 800 !important;
  border-bottom: 2px solid rgba(57,255,182,0.25) !important;
  font-size: 0.85rem !important;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

[data-testid="stDataFrame"] tbody tr:nth-child(odd) {
  background-color: rgba(255,255,255,0.025) !important;
}

[data-testid="stDataFrame"] tbody tr:hover {
  background: linear-gradient(90deg, rgba(57,255,182,0.08), rgba(79,142,247,0.08)) !important;
  transition: background 0.2s ease;
}

/* Dividers with gradient */
hr{ 
  border: none;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(57,255,182,0.3), transparent);
  margin: 2rem 0;
}

/* Enhanced tabs */
button[data-baseweb="tab"]{
  font-weight: 650;
  color: var(--muted);
  padding: 0.8rem 1.5rem !important;
  transition: all 0.3s ease;
}

button[data-baseweb="tab"]:hover{
  color: var(--text);
  background: rgba(57,255,182,0.05);
}

button[data-baseweb="tab"][aria-selected="true"]{
  color: var(--text);
  border-bottom: 3px solid var(--neon) !important;
  background: linear-gradient(180deg, rgba(57,255,182,0.08), transparent);
}

/* Enhanced links */
a, a:visited { 
  color: rgba(57,255,182,0.95);
  text-decoration: none;
  transition: all 0.2s ease;
}

a:hover {
  color: rgba(57,255,182,1);
  text-shadow: 0 0 8px rgba(57,255,182,0.5);
}

/* Download button special styling */
.stDownloadButton > button {
  background: linear-gradient(135deg, rgba(57,255,182,0.15), rgba(79,142,247,0.15)) !important;
  border: 1px solid rgba(57,255,182,0.40) !important;
}

.stDownloadButton > button:hover {
  border-color: rgba(57,255,182,0.65) !important;
  box-shadow: 0 8px 24px rgba(57,255,182,0.25) !important;
}

/* Enhanced expander */
[data-testid="stExpander"] {
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 14px;
  background: linear-gradient(180deg, rgba(16,24,36,0.4), rgba(11,15,20,0.6));
  overflow: hidden;
}

[data-testid="stExpander"] summary {
  font-weight: 650;
  padding: 1rem 1.2rem;
  background: rgba(93,91,255,0.06);
  transition: all 0.3s ease;
}

[data-testid="stExpander"] summary:hover {
  background: rgba(93,91,255,0.12);
}

/* Status badges */
.status-badge {
  display: inline-block;
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 650;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.status-api {
  background: linear-gradient(135deg, rgba(57,255,182,0.20), rgba(57,255,182,0.10));
  color: var(--neon);
  border: 1px solid rgba(57,255,182,0.30);
}

.status-cache {
  background: linear-gradient(135deg, rgba(79,142,247,0.20), rgba(79,142,247,0.10));
  color: var(--neon3);
  border: 1px solid rgba(79,142,247,0.30);
}

.status-error {
  background: linear-gradient(135deg, rgba(255,107,157,0.20), rgba(255,107,157,0.10));
  color: var(--accent);
  border: 1px solid rgba(255,107,157,0.30);
}

/* Loading animation */
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.loading {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

/* Toast notifications */
[data-testid="stToast"] {
  background: linear-gradient(135deg, var(--panel), var(--panel2)) !important;
  border: 1px solid rgba(57,255,182,0.30) !important;
  border-radius: 12px !important;
}
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


def _format_timestamp(ts: float) -> str:
    """Format timestamp to readable string"""
    dt = datetime.fromtimestamp(ts)
    return dt.strftime("%d/%m/%Y às %H:%M")


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

    expected = ["id", "nome", "siglaPartido", "siglaUf", "uri", "uriPartido", "urlFoto"]
    for c in expected:
        if c not in df.columns:
            df[c] = None

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
        with st.spinner("🔄 Carregando dados da API..."):
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
# Charts (matplotlib) - enhanced styling
# ----------------------------
def _style_dark_axes(ax):
    fg = "#E6EDF3"
    muted = "#B6C2CF"
    panel = "#0E141B"
    grid = (1, 1, 1, 0.10)

    ax.set_facecolor(panel)
    ax.tick_params(colors=muted, labelsize=10, width=0)
    
    for spine in ax.spines.values():
        spine.set_color((1, 1, 1, 0.14))
        spine.set_linewidth(1.5)

    ax.xaxis.label.set_color(muted)
    ax.yaxis.label.set_color(muted)
    ax.title.set_color(fg)
    ax.title.set_fontsize(13)
    ax.title.set_fontweight('bold')

    ax.grid(True, axis="x", color=grid, linewidth=1, alpha=0.5)
    ax.set_axisbelow(True)


def chart_partidos_bar(df: pd.DataFrame):
    counts = df["siglaPartido"].value_counts().head(20).sort_values()

    fig, ax = plt.subplots(figsize=(8.5, 5.5))
    fig.patch.set_facecolor("#0B0F14")
    _style_dark_axes(ax)

    neon_edge = (57 / 255, 1.0, 182 / 255, 0.90)
    fill = (57 / 255, 1.0, 182 / 255, 0.25)

    bars = ax.barh(counts.index, counts.values, color=fill, height=0.7)
    for b in bars:
        b.set_edgecolor(neon_edge)
        b.set_linewidth(1.6)

    ax.set_xlabel("Quantidade", fontsize=10, fontweight='600')
    ax.set_ylabel("")
    ax.set_title("Deputados por partido (Top 20)", pad=15)

    maxv = counts.max() if len(counts) else 0
    for i, v in enumerate(counts.values):
        ax.text(v + maxv * 0.015, i, str(int(v)), 
                va="center", ha="left", color="#E6EDF3", 
                fontsize=9, fontweight='600')

    ax.set_xlim(0, maxv * 1.12 if maxv else 1)
    fig.tight_layout()
    return fig


def chart_estados_bar(df: pd.DataFrame):
    counts = df["siglaUf"].value_counts().sort_values()

    fig, ax = plt.subplots(figsize=(8.5, 5.5))
    fig.patch.set_facecolor("#0B0F14")
    _style_dark_axes(ax)

    neon_edge = (79 / 255, 142 / 255, 247 / 255, 0.90)
    fill = (79 / 255, 142 / 255, 247 / 255, 0.25)

    bars = ax.barh(counts.index, counts.values, color=fill, height=0.7)
    for b in bars:
        b.set_edgecolor(neon_edge)
        b.set_linewidth(1.6)

    ax.set_xlabel("Quantidade", fontsize=10, fontweight='600')
    ax.set_ylabel("")
    ax.set_title("Deputados por UF", pad=15)

    maxv = counts.max() if len(counts) else 0
    for i, v in enumerate(counts.values):
        ax.text(v + maxv * 0.015, i, str(int(v)), 
                va="center", ha="left", color="#E6EDF3", 
                fontsize=9, fontweight='600')

    ax.set_xlim(0, maxv * 1.12 if maxv else 1)
    fig.tight_layout()
    return fig


def chart_top5_pizza(df: pd.DataFrame):
    counts = df["siglaPartido"].value_counts().head(5)

    fig, ax = plt.subplots(figsize=(6, 4.5))
    fig.patch.set_facecolor("#0B0F14")
    ax.set_facecolor("#0E141B")

    colors = [
        (57/255, 1.0, 182/255, 0.35),
        (79/255, 142/255, 247/255, 0.35),
        (93/255, 91/255, 1.0, 0.35),
        (255/255, 107/255, 157/255, 0.35),
        (138/255, 180/255, 248/255, 0.35),
    ]

    wedges, texts, autotexts = ax.pie(
        counts.values,
        labels=counts.index,
        autopct="%1.1f%%",
        startangle=90,
        pctdistance=0.78,
        labeldistance=1.08,
        colors=colors,
        textprops={"color": "#E6EDF3", "fontsize": 10, "fontweight": "600"},
        wedgeprops={
            "linewidth": 2,
            "edgecolor": (57/255, 255/255, 182/255, 0.85),
        },
    )

    centre_circle = plt.Circle((0, 0), 0.55, fc="#0E141B", ec=(1,1,1,0.1), linewidth=2)
    ax.add_artist(centre_circle)

    for t in autotexts:
        t.set_color("#E6EDF3")
        t.set_fontweight("700")
        t.set_fontsize(11)

    ax.set_title("Participação do Top 5 partidos", pad=20, fontweight='bold')
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
    with c1:
        st.metric("🏛️ Deputados", _fmt_int(total))
    with c2:
        st.metric("🎭 Partidos", _fmt_int(n_partidos))
    with c3:
        st.metric("🗺️ UFs", _fmt_int(n_ufs))
    with c4:
        st.metric("👥 Maior partido", f"{top_partido}", 
                 delta=f"{_fmt_int(top_qtd)} deputados" if top_partido != "-" else None)


def download_csv_button(df: pd.DataFrame, filename: str, label: str = "📥 Baixar CSV"):
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label=label,
        data=csv,
        file_name=filename,
        mime="text/csv",
        use_container_width=True,
    )


def deputy_details_card(row: dict):
    with st.container():
        col1, col2 = st.columns([1, 2])

        with col1:
            foto = row.get("urlFoto")
            if foto and str(foto) != "None":
                st.image(foto, use_container_width=True)
            else:
                st.info("📷 Foto indisponível")

        with col2:
            st.markdown(f"#### {row.get('nome', '-')}")
            st.write(f"**Partido:** {row.get('siglaPartido', '-')}")
            st.write(f"**UF:** {row.get('siglaUf', '-')}")
            
            uri = row.get("uri")
            if uri and str(uri) != "None":
                st.link_button("🔗 Ver dados na API", uri)


def render_table(df: pd.DataFrame, percent_col: str | None = None):
    """Enhanced table with percentage column"""
    dfx = df.copy()

    if percent_col and percent_col in dfx.columns:
        total = dfx[percent_col].sum()
        if total > 0:
            dfx["Percentual"] = (dfx[percent_col] / total * 100).round(1).astype(str) + "%"

    # Rename columns for better presentation
    column_names = {
        "siglaPartido": "Partido",
        "siglaUf": "UF",
        "qtdDeputados": "Quantidade"
    }
    dfx = dfx.rename(columns=column_names)

    st.dataframe(dfx, use_container_width=True, hide_index=True)


# ----------------------------
# Header
# ----------------------------
col_title, col_refresh = st.columns([4, 1])
with col_title:
    st.markdown('<h1 class="title-neon">🏛️ Análise de Deputados Federais</h1>', unsafe_allow_html=True)
    st.caption("Dashboard interativa para explorar a composição atual da Câmara: partidos, UFs e distribuição proporcional.")


# ----------------------------
# Sidebar
# ----------------------------
with st.sidebar:
    st.markdown("## ⚙️ Controles")

    ttl_minutes = st.number_input(
        "⏱️ Cache (minutos)",
        min_value=5,
        max_value=720,
        value=60,
        step=5,
        help="Tempo de validade do cache. Reduz chamadas à API.",
    )
    ttl_seconds = int(ttl_minutes * 60)

    col_a, col_b = st.columns(2)
    with col_a:
        refresh = st.button("🔄 Atualizar", use_container_width=True)
    with col_b:
        clear = st.button("🗑️ Limpar", use_container_width=True)

    if clear:
        st.session_state.cache_df = pd.DataFrame()
        st.session_state.cache_ts = 0.0
        st.session_state.cache_error = None
        st.toast("✅ Cache limpo com sucesso!", icon="🗑️")

    st.divider()
    st.markdown("## 🔍 Filtros")


# ----------------------------
# Load data
# ----------------------------
df, source = get_data(ttl_seconds=ttl_seconds, force_refresh=refresh)

if df.empty:
    err = st.session_state.get("cache_error")
    st.error("❌ Não foi possível carregar os dados agora.")
    if err:
        with st.expander("🔧 Detalhes técnicos"):
            st.code(err)
    st.stop()


# ----------------------------
# Filters
# ----------------------------
all_partidos = sorted(df["siglaPartido"].dropna().unique().tolist())
all_ufs = sorted(df["siglaUf"].dropna().unique().tolist())

with st.sidebar:
    partidos_sel = st.multiselect(
        "🎭 Partidos", 
        all_partidos, 
        default=[],
        help="Selecione um ou mais partidos para filtrar"
    )
    ufs_sel = st.multiselect(
        "🗺️ UFs", 
        all_ufs, 
        default=[],
        help="Selecione uma ou mais UFs para filtrar"
    )

    # Show active filters count
    active_filters = len(partidos_sel) + len(ufs_sel)
    if active_filters > 0:
        st.info(f"🎯 {active_filters} filtro(s) ativo(s)")

    st.divider()
    st.markdown("## 📊 Exibição")
    sort_by = st.selectbox(
        "📑 Ordenar por", 
        ["nome", "siglaPartido", "siglaUf"], 
        index=0,
        format_func=lambda x: {"nome": "Nome", "siglaPartido": "Partido", "siglaUf": "UF"}[x]
    )
    page_size = st.selectbox("📄 Linhas por página", [25, 50, 100, 200], index=1)

    st.divider()
    
    # Enhanced status display
    if source == "api":
        st.markdown('<span class="status-badge status-api">🟢 Atualizado agora</span>', unsafe_allow_html=True)
        if st.session_state.cache_ts:
            st.caption(f"⏰ {_format_timestamp(st.session_state.cache_ts)}")
    elif source == "cache":
        st.markdown('<span class="status-badge status-cache">🔵 Do cache</span>', unsafe_allow_html=True)
        if st.session_state.cache_ts:
            st.caption(f"⏰ {_format_timestamp(st.session_state.cache_ts)}")
    elif source == "cache_stale":
        st.markdown('<span class="status-badge status-error">🟡 Cache desatualizado</span>', unsafe_allow_html=True)
        st.caption("⚠️ API temporariamente indisponível")
    
    st.caption("📡 Fonte: Dados Abertos da Câmara")


df_f = apply_filters(df, partidos_sel=partidos_sel, ufs_sel=ufs_sel, sort_by=sort_by)

# Show filter results
if active_filters > 0:
    st.info(f"📊 Mostrando {len(df_f):,} de {len(df):,} deputados")


# ----------------------------
# Tabs
# ----------------------------
tabs = st.tabs(["📊 Visão geral", "🎭 Partidos", "🗺️ Estados", "👤 Deputados", "ℹ️ Sobre"])


# --- Visão geral ---
with tabs[0]:
    kpi_row(df_f)
    st.divider()

    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown("### 🎭 Deputados por partido")
        st.pyplot(chart_partidos_bar(df_f), clear_figure=True)

    with col2:
        st.markdown("### 🗺️ Deputados por UF")
        st.pyplot(chart_estados_bar(df_f), clear_figure=True)

    # Advanced analysis
    with st.expander("📈 Análises avançadas", expanded=False):
        colA, colB = st.columns([1.15, 1.35], gap="small")
        with colA:
            st.pyplot(chart_top5_pizza(df_f), clear_figure=True)
        with colB:
            st.markdown("### 💾 Exportação")
            st.caption("Baixe os dados considerando os filtros atuais.")
            download_csv_button(df_f, "deputados_filtrados.csv", label="📥 Baixar CSV (com filtros)")

    st.divider()
    download_csv_button(df_f, "deputados_filtrados.csv", label="📥 Baixar todos os dados")


# --- Partidos ---
with tabs[1]:
    st.markdown("### 🏆 Ranking de partidos")
    cont_partidos = counts_table(df_f["siglaPartido"], "siglaPartido")
    render_table(cont_partidos, percent_col="qtdDeputados")

    st.divider()
    download_csv_button(cont_partidos, "contagem_partidos.csv", label="📥 Baixar ranking de partidos")


# --- Estados ---
with tabs[2]:
    st.markdown("### 🏆 Ranking por UF")
    cont_ufs = counts_table(df_f["siglaUf"], "siglaUf")
    render_table(cont_ufs, percent_col="qtdDeputados")

    st.divider()
    download_csv_button(cont_ufs, "contagem_estados.csv", label="📥 Baixar ranking de UFs")


# --- Deputados ---
with tabs[3]:
    st.markdown("### 🔎 Explorar deputados")
    
    col_search, col_count = st.columns([3, 1])
    with col_search:
        search = st.text_input(
            "Buscar por nome", 
            value="", 
            placeholder="Digite um nome...",
            label_visibility="collapsed"
        )
    with col_count:
        st.metric("Total", len(df_f))

    df_view = df_f.copy()
    if search.strip():
        df_view = df_view[df_view["nome"].str.contains(search, case=False, na=False)]
        st.info(f"🔍 Encontrados {len(df_view)} resultado(s) para '{search}'")

    # Rename columns for display
    table_df = df_view[["nome", "siglaPartido", "siglaUf"]].copy()
    table_df = table_df.rename(columns={
        "nome": "Nome",
        "siglaPartido": "Partido",
        "siglaUf": "UF"
    })

    st.dataframe(
        table_df.head(page_size), 
        use_container_width=True, 
        hide_index=True,
        height=400
    )

    st.divider()
    st.markdown("### 👤 Detalhes do deputado")
    options = df_view["nome"].dropna().unique().tolist()
    selected = st.selectbox(
        "Selecionar deputado", 
        ["Selecione um deputado..."] + options,
        label_visibility="collapsed"
    )

    if selected and selected != "Selecione um deputado...":
        row = df_view[df_view["nome"] == selected].iloc[0].to_dict()
        deputy_details_card(row)

    st.divider()
    download_csv_button(df_view, "deputados_explorados.csv", label="📥 Baixar resultados da busca")


# --- Sobre ---
with tabs[4]:
    st.markdown(
        """
### 📋 Sobre este projeto

Esta dashboard foi desenvolvida para facilitar a análise da composição atual da Câmara dos Deputados, oferecendo:

- 📊 **Visualizações interativas** de distribuição por partido e UF
- 🔍 **Filtros avançados** para segmentação de dados
- 💾 **Exportação em CSV** para análises externas
- ⚡ **Cache inteligente** para melhor performance
- 🎨 **Interface moderna** com design futurista

#### 🛠️ Stack tecnológica
- **Python** - Linguagem de programação
- **Pandas** - Manipulação de dados
- **Streamlit** - Framework web
- **Matplotlib** - Visualizações

#### 📡 Fonte de dados
API de Dados Abertos da Câmara dos Deputados

---

💡 **Dica:** Para melhor performance em produção, mantenha o cache entre 30 e 120 minutos.
"""
    )
    
    with st.expander("🔧 Configurações recomendadas"):
        st.markdown("""
        - **Desenvolvimento local:** Cache de 5-15 minutos
        - **Produção (cloud):** Cache de 60-120 minutos
        - **Análises pontuais:** Use o botão "Atualizar" conforme necessário
        """)
    
    st.success("✨ Dashboard desenvolvida com foco em performance e experiência do usuário!")
