import streamlit as st
import pandas as pd

def kpi_row(df: pd.DataFrame):
    total = len(df)
    n_partidos = df["siglaPartido"].nunique(dropna=True)
    n_ufs = df["siglaUf"].nunique(dropna=True)

    top_partido = None
    top_qtd = 0
    if total > 0:
        vc = df["siglaPartido"].value_counts()
        if not vc.empty:
            top_partido = vc.index[0]
            top_qtd = int(vc.iloc[0])

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total de deputados", f"{total}")
    c2.metric("Partidos", f"{n_partidos}")
    c3.metric("UFs", f"{n_ufs}")
    c4.metric("Maior partido", f"{top_partido or '-'}", delta=f"{top_qtd} deputados" if top_partido else None)

def download_section(df: pd.DataFrame, label_prefix: str):
    st.markdown("#### Downloads")
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Baixar CSV",
        data=csv,
        file_name=f"{label_prefix}.csv",
        mime="text/csv",
        use_container_width=True,
    )

def deputy_details_card(row: dict):
    col1, col2 = st.columns([1, 2])

    with col1:
        foto = row.get("urlFoto")
        if foto:
            st.image(foto, use_container_width=True)
        else:
            st.info("Sem foto disponível.")

    with col2:
        st.markdown(f"### {row.get('nome', '-')}")
        st.write(f"**Partido:** {row.get('siglaPartido', '-')}")
        st.write(f"**UF:** {row.get('siglaUf', '-')}")
        uri = row.get("uri")
        if uri:
            st.link_button("🔗 Ver na API (uri)", uri)

