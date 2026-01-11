import requests
import pandas as pd
import streamlit as st

BASE_URL = "https://dadosabertos.camara.leg.br/api/v2"

@st.cache_data(show_spinner=False)
def fetch_deputados_df(ttl_seconds: int = 3600, force_refresh: bool = False) -> pd.DataFrame:
    # truque: quando force_refresh muda, o cache invalida
    _ = force_refresh

    # TTL do cache (Streamlit recomenda ttl p/ chamadas de API) :contentReference[oaicite:4]{index=4}
    # OBS: o TTL é aplicado pelo decorator via parâmetros de cache do Streamlit,
    # então usamos st.cache_data e controlamos invalidando com force_refresh.
    # Se quiser TTL real por tempo, dá pra colocar @st.cache_data(ttl=ttl_seconds),
    # mas aí ttl_seconds vira parte da assinatura.

    url = f"{BASE_URL}/deputados"
    params = {"itens": 1000, "ordem": "ASC", "ordenarPor": "nome"}

    try:
        r = requests.get(url, params=params, timeout=30)
        r.raise_for_status()
        data = r.json().get("dados", [])
    except Exception:
        return pd.DataFrame()

    if not data:
        return pd.DataFrame()

    df = pd.DataFrame(data)

    # Normalização mínima (garante colunas esperadas)
    expected = ["id", "nome", "siglaPartido", "siglaUf", "uri", "uriPartido", "urlFoto"]
    for c in expected:
        if c not in df.columns:
            df[c] = None

    return df

def apply_filters(df: pd.DataFrame, partidos_sel, ufs_sel, sort_by: str) -> pd.DataFrame:
    out = df.copy()

    if partidos_sel:
        out = out[out["siglaPartido"].isin(partidos_sel)]
    if ufs_sel:
        out = out[out["siglaUf"].isin(ufs_sel)]

    if sort_by in out.columns:
        out = out.sort_values(sort_by, kind="stable")

    return out.reset_index(drop=True)

