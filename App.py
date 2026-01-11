# app.py
# Futuristic / minimal (dark) Streamlit dashboard with subtle neon accents
# + higher-contrast bar charts
# + "Destaques" cards (Top 5) instead of donut chart
# + elegant tables (zebra + hover + header polish + % column)
# + automated "Testes" tab (smoke tests) to validate core functionalities
# + CSV downloads: (1) filtros atuais, (2) base completa (sem filtros)  ✅ agora são diferentes
#
# Requisitos: streamlit, pandas, requests, matplotlib

import time
import requests
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.figure import Figure


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
  border-bottom: 1px solid rgba(57,255,182,0.40);
  box-shadow: 0 14px 32px rgba(57,255,182,0.08);
}

/* Metric cards */
[data-testid="metric-container"]{
  background: radial-gradient(1200px 160px at 10% 0%, rgba(93,91,255,0.14), rgba(0,0,0,0) 55%),
              linear-gradient(180deg, var(--panel) 0%, #0B1017 100%);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 16px;
  padding: 1rem 1rem;
}

/* Buttons */
.stButton > button{
  border-radius: 12px;
  font-weight: 650;
  padding: 0.60rem 0.90rem;
  border: 1px solid rgba(79,142,247,0.28);
  background: linear-gradient(180deg, rgba(79,142,247,0.14) 0%, rgba(79,142,247,0.05) 100%);
}
.stButton > button:hover{
  border-color: rgba(57,255,182,0.42);
  box-shadow: 0 10px 28px rgba(57,255,182,0.12);
}

/* Inputs */
[data-baseweb="select"] > div, [data-baseweb="input"] input{
  border-radius: 12px !important;
  border-color: rgba(255,255,255,0.12) !important;
  background-color: rgba(16,24,36,0.58) !important;
}

/* Dataframe container */
[data-testid="stDataFrame"]{
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 16px;
  overflow: hidden;
}

/* Dataframe: header + zebra + hover */
[data-testid="stDataFrame"] thead tr th {
  background: rgba(93, 91, 255, 0.12) !important;
  color: #E6EDF3 !important;
  font-weight: 800 !important;
  border-bottom: 1px solid rgba(255,255,255,0.12) !important;
}
[data-testid="stDataFrame"] tbody tr:nth-child(odd) {
  background-color: rgba(255,255,255,0.02) !important;
}
[data-testid="stDataFrame"] tbody tr:hover {
  background-color: rgba(57,255,182,0.07) !important;
}

/* Dividers */
hr{ border-color: rgba(255,255,255,0.08); }

/* Tabs */
button[data-baseweb="tab"]{
  font-weight: 650;
  color: var(--muted);
}
button[data-baseweb="tab"][aria-selected="true"]{
  color: var(--text);
  border-bottom: 2px solid rgba(57,255,182,0.85) !important;
}

/* Links */
a, a:visited { color: rgba(57,255,182,0.92); }

/* Destaques cards */
.hi-wrap{
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
}
.hi-card{
  border-radius: 16px;
  border: 1px solid rgba(255,255,255,0.10);
  background:
    radial-gradient(900px 140px at 10% 0%, rgba(57,255,182,0.14), rgba(0,0,0,0) 60%),
    linear-gradient(180deg, rgba(16,24,36,0.70) 0%, rgba(14,20,27,0.70) 100%);
  padding: 14px 14px 12px 14px;
  box-shadow: 0 18px 40px rgba(0,0,0,0.22);
}
.hi-top{
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:10px;
  margin-bottom: 8px;
}
.hi-pill{
  font-size: 12px;
  color: rgba(230,237,243,0.90);
  padding: 4px 10px;
  border-radius: 999px;
  border: 1px solid rgba(57,255,182,0.22);
  background: rgba(57,255,182,0.08);
  white-space: nowrap;
}
.hi-title{
  font-weight: 800;
  font-size: 16px;
  letter-spacing: -0.02em;
  color: #E6EDF3;
}
.hi-metrics{
  display:flex;
  gap:12px;
  flex-wrap:wrap;
}
.hi-metric{
  font-size: 13px;
  color: rgba(230,237,243,0.80);
}
.hi-metric b{
  color: #E6EDF3;
  font-weight: 800;
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


def _to_csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8")


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
# Charts (matplotlib) - higher contrast + subtle neon
# ----------------------------
def _style_dark_axes(ax):
    fg = "#E6EDF3"
    muted = "#B6C2CF"
    panel = "#0E141B"
    grid = (1, 1, 1, 0.10)

    ax.set_facecolor(panel)
    ax.tick_params(colors=muted, labelsize=10)
    for spine in ax.spines.values():
        spine.set_color((1, 1, 1, 0.14))

    ax.xaxis.label.set_color(muted)
    ax.yaxis.label.set_color(muted)
    ax.title.set_color(fg)

    ax.grid(True, axis="x", color=grid, linewidth=1)
    ax.set_axisbelow(True)


def chart_partidos_bar(df: pd.DataFrame) -> Figure:
    counts = df["siglaPartido"].value_counts().head(20).sort_values()

    fig, ax = plt.subplots(figsize=(8.2, 5.2))
    fig.patch.set_facecolor("#0B0F14")
    _style_dark_axes(ax)

    neon_edge = (57 / 255, 1.0, 182 / 255, 0.85)
    fill = (57 / 255, 1.0, 182 / 255, 0.22)

    bars = ax.barh(counts.index, counts.values, color=fill)
    for b in bars:
        b.set_edgecolor(neon_edge)
        b.set_linewidth(1.4)

    ax.set_xlabel("Quantidade")
    ax.set_ylabel("")
    ax.set_title("Deputados por partido (Top 20)")

    maxv = counts.max() if len(counts) else 0
    for i, v in enumerate(counts.values):
        ax.text(v + maxv * 0.01, i, str(int(v)), va="center", color="#E6EDF3", fontsize=9)

    ax.set_xlim(0, maxv * 1.10 if maxv else 1)
    fig.tight_layout()
    return fig


def chart_estados_bar(df: pd.DataFrame) -> Figure:
    counts = df["siglaUf"].value_counts().sort_values()

    fig, ax = plt.subplots(figsize=(8.2, 5.2))
    fig.patch.set_facecolor("#0B0F14")
    _style_dark_axes(ax)

    neon_edge = (79 / 255, 142 / 255, 247 / 255, 0.85)
    fill = (79 / 255, 142 / 255, 247 / 255, 0.22)

    bars = ax.barh(counts.index, counts.values, color=fill)
    for b in bars:
        b.set_edgecolor(neon_edge)
        b.set_linewidth(1.4)

    ax.set_xlabel("Quantidade")
    ax.set_ylabel("")
    ax.set_title("Deputados por UF")

    maxv = counts.max() if len(counts) else 0
    for i, v in enumerate(counts.values):
        ax.text(v + maxv * 0.01, i, str(int(v)), va="center", color="#E6EDF3", fontsize=9)

    ax.set_xlim(0, maxv * 1.10 if maxv else 1)
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


def download_csv_button(df: pd.DataFrame, filename: str, label: str):
    st.download_button(
        label=label,
        data=_to_csv_bytes(df),
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
            st.link_button("Ver dados na API", uri)


def render_table(df: pd.DataFrame, percent_col: str | None = None):
    dfx = df.copy()

    if percent_col and percent_col in dfx.columns:
        total = dfx[percent_col].sum()
        if total > 0:
            dfx["%"] = (dfx[percent_col] / total * 100).round(1)

    fmt_map = {}
    if "qtdDeputados" in dfx.columns:
        fmt_map["qtdDeputados"] = "{:,.0f}".format
    if "%" in dfx.columns:
        fmt_map["%"] = "{:.1f}%".format

    styler = dfx.style.format(fmt_map).set_properties(**{"font-size": "14px"})
    st.dataframe(styler, use_container_width=True, hide_index=True)


def render_highlights_top5(df: pd.DataFrame):
    """
    Destaques (Top 5) em cards:
    - sem gráfico (menos "ruído")
    - visual futurista com bordas arredondadas
    - mostra contagem e % na base filtrada atual
    """
    total = len(df)
    vc = df["siglaPartido"].value_counts().head(5)

    if total == 0 or vc.empty:
        st.info("Sem dados para exibir destaques.")
        return

    # Monta HTML dos cards (mais controle visual)
    cards = []
    for i, (sigla, qtd) in enumerate(vc.items(), start=1):
        pct = (qtd / total) * 100 if total else 0
        cards.append(
            f"""
            <div class="hi-card">
              <div class="hi-top">
                <div class="hi-title">{sigla}</div>
                <div class="hi-pill">Top {i}</div>
              </div>
              <div class="hi-metrics">
                <div class="hi-metric"><b>{qtd}</b> deputados</div>
                <div class="hi-metric"><b>{pct:.1f}%</b> da base</div>
              </div>
            </div>
            """
        )

    st.markdown(f'<div class="hi-wrap">{"".join(cards)}</div>', unsafe_allow_html=True)


# ----------------------------
# Automated tests (inside app)
# ----------------------------
def run_smoke_tests(df_base: pd.DataFrame, df_filtered: pd.DataFrame) -> list[dict]:
    results = []

    def add(name: str, ok: bool, detail: str = ""):
        results.append({"name": name, "ok": ok, "detail": detail})

    # 1) Dataset sanity
    required_cols = {"id", "nome", "siglaPartido", "siglaUf", "uri", "urlFoto"}
    missing = required_cols - set(df_base.columns)
    add(
        "Colunas essenciais presentes",
        ok=len(missing) == 0,
        detail="" if len(missing) == 0 else f"Faltando: {sorted(list(missing))}",
    )

    add("Base não vazia", ok=len(df_base) > 0, detail=f"Linhas: {len(df_base)}")

    # 2) Filtering sanity
    add("Filtro não cria linhas novas", ok=len(df_filtered) <= len(df_base), detail=f"{len(df_filtered)} <= {len(df_base)}")

    # 3) Charts creation
    try:
        f1 = chart_partidos_bar(df_filtered if len(df_filtered) else df_base)
        add("Gráfico Partidos (bar) gera Figure", ok=isinstance(f1, Figure))
    except Exception as e:
        add("Gráfico Partidos (bar) gera Figure", ok=False, detail=str(e))

    try:
        f2 = chart_estados_bar(df_filtered if len(df_filtered) else df_base)
        add("Gráfico UFs (bar) gera Figure", ok=isinstance(f2, Figure))
    except Exception as e:
        add("Gráfico UFs (bar) gera Figure", ok=False, detail=str(e))

    # 4) Tables
    try:
        t1 = counts_table(df_base["siglaPartido"], "siglaPartido")
        add("Tabela contagem partidos OK", ok=("siglaPartido" in t1.columns and "qtdDeputados" in t1.columns and len(t1) > 0))
    except Exception as e:
        add("Tabela contagem partidos OK", ok=False, detail=str(e))

    try:
        t2 = counts_table(df_base["siglaUf"], "siglaUf")
        add("Tabela contagem UFs OK", ok=("siglaUf" in t2.columns and "qtdDeputados" in t2.columns and len(t2) > 0))
    except Exception as e:
        add("Tabela contagem UFs OK", ok=False, detail=str(e))

    # 5) CSV difference (this checks your issue)
    try:
        b_filtered = _to_csv_bytes(df_filtered)
        b_full = _to_csv_bytes(df_base)
        different = b_filtered != b_full  # if filters applied, should differ; if no filters, can be equal
        add(
            "CSV 'com filtros' difere da base completa (quando filtros ativos)",
            ok=(different or len(df_filtered) == len(df_base)),
            detail=("Diferentes" if different else "Iguais (ok se nenhum filtro foi aplicado)"),
        )
    except Exception as e:
        add("CSV diff check", ok=False, detail=str(e))

    return results


# ----------------------------
# Header
# ----------------------------
st.markdown('<h1 class="title-neon">Análise de Deputados Federais</h1>', unsafe_allow_html=True)
st.caption("Dashboard para explorar a composição atual da Câmara: partidos, UFs, filtros e exportação.")


# ----------------------------
# Sidebar
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
# Filters
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
# Tabs
# ----------------------------
tabs = st.tabs(["Visão geral", "Partidos", "Estados", "Deputados", "Testes", "Sobre"])


# --- Visão geral ---
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

    # Advanced analysis (Option A): Destaques + Exportação
    with st.expander("Análises avançadas", expanded=False):
        colA, colB = st.columns([1.15, 1.35], gap="small")

        with colA:
            st.markdown("### Destaques (Top 5 partidos)")
            st.caption("Resumo rápido com base nos filtros atuais.")
            render_highlights_top5(df_f)

        with colB:
            st.markdown("### Exportação")
            st.caption("Baixe os dados considerando os filtros atuais (não é a base completa).")
            download_csv_button(df_f, "deputados_filtrados.csv", "Baixar CSV (com filtros)")

            st.divider()
            st.caption("Baixe a base completa (sem filtros).")
            download_csv_button(df, "deputados_base_completa.csv", "Baixar CSV (base completa)")

    st.divider()
    # Atalhos (fora do expander) — agora explícitos e diferentes
    cA, cB = st.columns(2, gap="small")
    with cA:
        download_csv_button(df_f, "deputados_filtrados.csv", "Baixar CSV (com filtros)")
    with cB:
        download_csv_button(df, "deputados_base_completa.csv", "Baixar CSV (base completa)")


# --- Partidos ---
with tabs[1]:
    st.markdown("### Ranking de partidos")
    cont_partidos = counts_table(df_f["siglaPartido"], "siglaPartido")
    render_table(cont_partidos, percent_col="qtdDeputados")

    st.divider()
    download_csv_button(cont_partidos, "contagem_partidos.csv", "Baixar CSV (ranking partidos)")


# --- Estados ---
with tabs[2]:
    st.markdown("### Ranking por UF")
    cont_ufs = counts_table(df_f["siglaUf"], "siglaUf")
    render_table(cont_ufs, percent_col="qtdDeputados")

    st.divider()
    download_csv_button(cont_ufs, "contagem_estados.csv", "Baixar CSV (ranking UFs)")


# --- Deputados ---
with tabs[3]:
    st.markdown("### Explorar deputados")
    search = st.text_input("Buscar por nome", value="", placeholder="Digite um nome...")

    df_view = df_f.copy()
    if search.strip():
        df_view = df_view[df_view["nome"].str.contains(search, case=False, na=False)]

    preferred_cols = ["nome", "siglaPartido", "siglaUf"]
    cols = [c for c in preferred_cols if c in df_view.columns]
    table_df = df_view[cols] if cols else df_view

    st.dataframe(table_df.head(page_size), use_container_width=True, hide_index=True)

    st.divider()
    st.markdown("### Detalhes")
    options = df_view["nome"].dropna().unique().tolist()
    selected = st.selectbox("Selecionar deputado", [""] + options)

    if selected:
        row = df_view[df_view["nome"] == selected].iloc[0].to_dict()
        deputy_details_card(row)

    st.divider()
    download_csv_button(df_view, "deputados_explorados.csv", "Baixar CSV (resultado atual)")


# --- Testes automatizados (smoke tests) ---
with tabs[4]:
    st.markdown("### Testes automatizados (smoke tests)")
    st.caption(
        "Essa aba valida automaticamente as principais funcionalidades: "
        "carregamento, filtros, gráficos, tabelas e exportação."
    )

    run = st.button("Rodar testes agora", use_container_width=True)

    if run:
        results = run_smoke_tests(df_base=df, df_filtered=df_f)

        ok_count = sum(1 for r in results if r["ok"])
        total = len(results)

        if ok_count == total:
            st.success(f"✅ {ok_count}/{total} testes passaram.")
        else:
            st.warning(f"⚠️ {ok_count}/{total} testes passaram. Veja detalhes abaixo.")

        for r in results:
            if r["ok"]:
                st.success(r["name"])
            else:
                st.error(r["name"])
            if r["detail"]:
                st.caption(r["detail"])

        st.divider()
        st.caption("Dica: para testes de CI de verdade, o ideal é criar arquivos de teste com pytest no repositório.")


# --- Sobre ---
with tabs[5]:
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
