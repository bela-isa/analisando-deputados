import matplotlib.pyplot as plt
import pandas as pd

def chart_partidos_bar(df: pd.DataFrame):
    counts = df["siglaPartido"].value_counts().head(20)
    fig, ax = plt.subplots()
    counts.sort_values().plot(kind="barh", ax=ax)
    ax.set_xlabel("Quantidade de deputados")
    ax.set_ylabel("Partido")
    ax.set_title("Top 20 partidos")
    fig.tight_layout()
    return fig

def chart_estados_bar(df: pd.DataFrame):
    counts = df["siglaUf"].value_counts()
    fig, ax = plt.subplots()
    counts.sort_values().plot(kind="barh", ax=ax)
    ax.set_xlabel("Quantidade de deputados")
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

