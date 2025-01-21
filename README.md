# Análise de Dados: Deputados Federais

Este projeto realiza uma análise dos dados dos deputados federais brasileiros utilizando a API de Dados Abertos da Câmara dos Deputados.

## Funcionalidades

O projeto analisa:
- Distribuição de deputados por partido (gráfico de barras e pizza)
- Distribuição de deputados por estado (gráfico de barras)
- Análise dos 5 maiores partidos

## Requisitos

- Python 3.8+
- Bibliotecas Python listadas em `requirements.txt`

## Instalação

1. Clone este repositório
2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
.\venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Uso

Execute o script principal:
```bash
python analise_deputados.py
```

## Resultados

### Arquivos CSV
- `resultados/deputados.csv`: Lista completa dos deputados
- `resultados/contagem_partidos.csv`: Quantidade de deputados por partido
- `resultados/contagem_estados.csv`: Quantidade de deputados por estado

### Visualizações
- `resultados/deputados_por_partido.png`: Distribuição de deputados por partido (barras)
- `resultados/deputados_por_estado.png`: Distribuição de deputados por estado (barras)
- `resultados/maiores_partidos_pizza.png`: Top 5 maiores partidos (pizza)

## Documentação

- `ANALISES.md`: Documentação detalhada das análises e visualizações geradas
  - Explicação de cada arquivo gerado
  - Guia de interpretação dos gráficos
  - Observações importantes sobre os dados

## Fonte dos Dados

Os dados são obtidos através da API de Dados Abertos da Câmara dos Deputados:
https://dadosabertos.camara.leg.br/swagger/api.html

## Limitações

- Os dados são limitados às informações básicas dos deputados
- A API de proposições não está disponível no momento
- Os dados refletem apenas a composição atual da Câmara

## Contribuição

Para contribuir com o projeto:
1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-analise`)
3. Faça commit das mudanças (`git commit -am 'Adiciona nova análise'`)
4. Faça push para a branch (`git push origin feature/nova-analise`)
5. Abra um Pull Request 