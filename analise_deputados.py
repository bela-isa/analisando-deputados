import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import json
from datetime import datetime
import os
from dotenv import load_dotenv

# Configurar o estilo dos gráficos
plt.style.use('seaborn-v0_8')  # Usando um estilo compatível
sns.set_theme()  # Aplicar tema do seaborn

def obter_dados_deputados():
    """
    Obtém dados dos deputados através da API da Câmara
    """
    print("Coletando dados dos deputados...")
    url = "https://dadosabertos.camara.leg.br/api/v2/deputados"
    
    try:
        # Fazer requisição à API
        response = requests.get(url)
        response.raise_for_status()
        
        # Converter resposta para DataFrame
        dados = response.json()['dados']
        df = pd.DataFrame(dados)
        
        print(f"Foram encontrados {len(df)} deputados")
        print("\nColunas disponíveis:")
        print(df.columns.tolist())
        return df
    
    except Exception as e:
        print(f"Erro ao coletar dados: {str(e)}")
        return pd.DataFrame()

def obter_proposicoes_deputado(id_deputado):
    """
    Obtém as proposições de um deputado específico
    """
    url = f"https://dadosabertos.camara.leg.br/api/v2/proposicoes"
    params = {
        'autor': id_deputado,
        'ordenarPor': 'id',
        'itens': 100
    }
    
    try:
        print(f"Fazendo requisição para: {url}")
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        dados = response.json()['dados']
        print(f"Encontradas {len(dados)} proposições")
        
        # Converter para DataFrame e selecionar colunas relevantes
        df = pd.DataFrame(dados)
        if not df.empty:
            colunas = ['id', 'siglaTipo', 'numero', 'ano', 'ementa', 'statusProposicao']
            df = df[colunas]
            return df
        else:
            print("Nenhuma proposição encontrada")
            return pd.DataFrame()
    except Exception as e:
        print(f"Erro ao obter proposições: {str(e)}")
        print(f"URL completa: {response.url if 'response' in locals() else url}")
        return pd.DataFrame()

def analisar_partidos(df):
    """
    Analisa a distribuição de deputados por partido
    """
    print("\nAnalisando distribuição por partido...")
    
    # Contagem de deputados por partido
    partido_counts = df['siglaPartido'].value_counts()
    
    # Criar gráfico
    plt.figure(figsize=(15, 8))
    partido_counts.plot(kind='bar')
    plt.title('Distribuição de Deputados por Partido')
    plt.xlabel('Partido')
    plt.ylabel('Número de Deputados')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Salvar gráfico
    plt.savefig('resultados/deputados_por_partido.png')
    plt.close()
    
    return partido_counts

def analisar_estados(df):
    """
    Analisa a distribuição de deputados por estado
    """
    print("\nAnalisando distribuição por estado...")
    
    # Contagem de deputados por estado
    estado_counts = df['siglaUf'].value_counts()
    
    # Criar gráfico
    plt.figure(figsize=(15, 8))
    estado_counts.plot(kind='bar')
    plt.title('Distribuição de Deputados por Estado')
    plt.xlabel('Estado')
    plt.ylabel('Número de Deputados')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Salvar gráfico
    plt.savefig('resultados/deputados_por_estado.png')
    plt.close()
    
    return estado_counts

def analisar_proposicoes(df):
    """
    Analisa as proposições de cada deputado
    """
    print("\nAnalisando proposições dos deputados...")
    print("(Isso pode levar alguns minutos...)")
    
    todas_proposicoes = []
    total_deputados = len(df)
    
    # Limitar a 10 deputados para teste
    for idx, deputado in df.head(10).iterrows():
        print(f"\nProgresso: {idx+1}/{total_deputados} - Coletando proposições de {deputado['nome']}...")
        proposicoes = obter_proposicoes_deputado(deputado['id'])
        if not proposicoes.empty:
            proposicoes['autor'] = deputado['nome']
            proposicoes['partido'] = deputado['siglaPartido']
            proposicoes['estado'] = deputado['siglaUf']
            todas_proposicoes.append(proposicoes)
            print(f"Adicionadas {len(proposicoes)} proposições")
    
    if todas_proposicoes:
        print("\nConcatenando todas as proposições...")
        df_proposicoes = pd.concat(todas_proposicoes, ignore_index=True)
        print(f"Total de proposições coletadas: {len(df_proposicoes)}")
        
        # Análises adicionais
        print("\nEstatísticas das proposições:")
        print(f"Total de proposições: {len(df_proposicoes)}")
        print("\nTipos de proposições mais comuns:")
        print(df_proposicoes['siglaTipo'].value_counts().head())
        
        # Criar gráfico de proposições por tipo
        plt.figure(figsize=(15, 8))
        df_proposicoes['siglaTipo'].value_counts().plot(kind='bar')
        plt.title('Tipos de Proposições mais Comuns')
        plt.xlabel('Tipo de Proposição')
        plt.ylabel('Quantidade')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('resultados/tipos_proposicoes.png')
        plt.close()
        
        return df_proposicoes
    else:
        print("\nNenhuma proposição foi encontrada!")
        return pd.DataFrame()

def salvar_resultados(df, partido_counts, estado_counts, df_proposicoes):
    """
    Salva os resultados em arquivos CSV
    """
    # Criar diretório para resultados se não existir
    if not os.path.exists('resultados'):
        os.makedirs('resultados')
    
    # Salvar DataFrame principal
    df.to_csv('resultados/deputados.csv', index=False)
    
    # Salvar contagens em arquivos separados
    partido_counts.to_csv('resultados/contagem_partidos.csv')
    estado_counts.to_csv('resultados/contagem_estados.csv')
    
    if not df_proposicoes.empty:
        # Salvar proposições completas
        df_proposicoes.to_csv('resultados/proposicoes.csv', index=False)
        
        # Salvar resumos
        resumo_por_estado = df_proposicoes.groupby('estado').size()
        resumo_por_estado.to_csv('resultados/proposicoes_por_estado.csv')
        
        resumo_por_partido = df_proposicoes.groupby('partido').size()
        resumo_por_partido.to_csv('resultados/proposicoes_por_partido.csv')
        
        resumo_por_tipo = df_proposicoes.groupby('siglaTipo').size()
        resumo_por_tipo.to_csv('resultados/proposicoes_por_tipo.csv')
        
        # Top 10 deputados com mais proposições
        top_autores = df_proposicoes.groupby('autor').size().sort_values(ascending=False).head(10)
        top_autores.to_csv('resultados/top_10_autores.csv')
    
    print("\nResultados salvos no diretório 'resultados'")

def explicar_tipos_proposicoes():
    """
    Retorna um dicionário com explicações dos tipos mais comuns de proposições
    """
    return {
        'PL': 'Projeto de Lei - Proposta de nova lei ou alteração de lei existente',
        'REQ': 'Requerimento - Solicitação de providências, informações ou ações',
        'PFC': 'Proposta de Fiscalização e Controle - Para fiscalizar atos do Poder Executivo',
        'PDL': 'Projeto de Decreto Legislativo - Para regular matérias de competência exclusiva do Congresso',
        'PEC': 'Proposta de Emenda à Constituição - Para modificar a Constituição Federal',
        'INC': 'Indicação - Sugestão de medidas a outros Poderes',
        'RIC': 'Requerimento de Informação - Pedido de informações a Ministros de Estado',
        'VTS': 'Voto em Separado - Voto alternativo ao do relator em comissão',
        'EMC': 'Emenda - Proposta de alteração a uma proposição',
        'PLP': 'Projeto de Lei Complementar - Para regulamentar artigos da Constituição'
    }

def analisar_atividade_deputados(df_proposicoes):
    """
    Analisa detalhadamente a atividade dos deputados
    """
    if df_proposicoes.empty:
        return
        
    print("\nAnálise detalhada da atividade parlamentar:")
    print("-" * 50)
    
    # Contagem total de proposições por deputado
    atividade_total = df_proposicoes.groupby('autor').size().sort_values(ascending=False)
    
    # Top 10 deputados mais ativos
    print("\nTop 10 deputados com mais proposições apresentadas:")
    print("-" * 50)
    for i, (deputado, total) in enumerate(atividade_total.head(10).items(), 1):
        partido = df_proposicoes[df_proposicoes['autor'] == deputado]['partido'].iloc[0]
        estado = df_proposicoes[df_proposicoes['autor'] == deputado]['estado'].iloc[0]
        tipos = df_proposicoes[df_proposicoes['autor'] == deputado]['siglaTipo'].value_counts()
        
        print(f"{i}. {deputado} ({partido}/{estado})")
        print(f"   Total de proposições: {total}")
        print("   Tipos de proposições:")
        for tipo, quantidade in tipos.items():
            print(f"   - {tipo}: {quantidade}")
        print()
    
    # Explicar os tipos de proposições
    print("\nTipos de proposições mais comuns:")
    print("-" * 50)
    tipos_explicacao = explicar_tipos_proposicoes()
    tipos_contagem = df_proposicoes['siglaTipo'].value_counts()
    
    for tipo, quantidade in tipos_contagem.items():
        if tipo in tipos_explicacao:
            print(f"{tipo}: {quantidade} proposições")
            print(f"   {tipos_explicacao[tipo]}")
        else:
            print(f"{tipo}: {quantidade} proposições")
        print()

def analisar_proposicoes_importantes(df_proposicoes):
    """
    Analisa e mostra os detalhes das proposições mais importantes (PLs, PECs, etc.)
    """
    if df_proposicoes.empty:
        return
        
    # Tipos importantes de proposições
    tipos_importantes = ['PL', 'PEC', 'PLP', 'PDL']
    
    print("\nDetalhes das Proposições Importantes:")
    print("=" * 80)
    
    for tipo in tipos_importantes:
        proposicoes_tipo = df_proposicoes[df_proposicoes['siglaTipo'] == tipo]
        
        if not proposicoes_tipo.empty:
            print(f"\n{tipo} - {explicar_tipos_proposicoes()[tipo]}")
            print("-" * 80)
            
            for _, prop in proposicoes_tipo.iterrows():
                print(f"\nAutor: {prop['autor']} ({prop['partido']}/{prop['estado']})")
                print(f"Número: {prop['siglaTipo']} {prop['numero']}/{prop['ano']}")
                print(f"Ementa: {prop['ementa']}")
                print(f"Status: {prop['statusProposicao']['descricaoSituacao']}")
                print("-" * 40)

def criar_graficos_adicionais(df_proposicoes, partido_counts, estado_counts):
    """
    Cria gráficos adicionais para melhor visualização dos dados
    """
    if not os.path.exists('resultados'):
        os.makedirs('resultados')
    
    # Gráfico de pizza para os 5 maiores partidos
    plt.figure(figsize=(12, 8))
    top_5_partidos = partido_counts.head()
    outros = pd.Series({'Outros': partido_counts[5:].sum()})
    partidos_plot = pd.concat([top_5_partidos, outros])
    
    plt.pie(partidos_plot.values, labels=partidos_plot.index, autopct='%1.1f%%')
    plt.title('Distribuição dos 5 Maiores Partidos', pad=20, fontsize=14)  # Aumentado o padding do título
    plt.axis('equal')
    plt.savefig('resultados/maiores_partidos_pizza.png', bbox_inches='tight', pad_inches=0.5)  # Aumentado o padding geral
    plt.close()

def main():
    # Obter dados
    df_deputados = obter_dados_deputados()
    
    if df_deputados.empty:
        print("Não foi possível obter dados dos deputados")
        return
    
    # Realizar análises
    partido_counts = analisar_partidos(df_deputados)
    estado_counts = analisar_estados(df_deputados)
    
    # Criar gráficos adicionais
    criar_graficos_adicionais(None, partido_counts, estado_counts)
    
    # Mostrar alguns resultados
    print("\nTop 5 partidos com mais deputados:")
    print(partido_counts.head())
    
    print("\nDistribuição por estado:")
    print(estado_counts)
    
    # Salvar resultados básicos
    if not os.path.exists('resultados'):
        os.makedirs('resultados')
    
    df_deputados.to_csv('resultados/deputados.csv', index=False)
    partido_counts.to_csv('resultados/contagem_partidos.csv')
    estado_counts.to_csv('resultados/contagem_estados.csv')
    
    print("\nAnálise concluída! Os arquivos foram salvos no diretório 'resultados'")
    print("\nArquivos gerados:")
    print("- deputados.csv: Lista completa dos deputados")
    print("- contagem_partidos.csv: Quantidade de deputados por partido")
    print("- contagem_estados.csv: Quantidade de deputados por estado")
    print("\nGráficos gerados:")
    print("- deputados_por_partido.png: Distribuição de deputados por partido (barras)")
    print("- deputados_por_estado.png: Distribuição de deputados por estado (barras)")
    print("- maiores_partidos_pizza.png: Top 5 maiores partidos (pizza)")

if __name__ == "__main__":
    main() 