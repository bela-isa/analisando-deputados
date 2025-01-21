# Análise de Dados dos Deputados Federais

Este documento explica todas as análises e visualizações geradas pelo script de análise de dados dos deputados federais.

## Arquivos CSV Gerados

### Dados Básicos
- `deputados.csv`: Lista completa dos deputados com suas informações básicas
- `contagem_partidos.csv`: Quantidade de deputados por partido
- `contagem_estados.csv`: Quantidade de deputados por estado

## Visualizações Geradas

### 1. Distribuição por Partido (Barras)
- **Arquivo**: `deputados_por_partido.png`
- **Descrição**: Gráfico de barras mostrando a quantidade de deputados em cada partido
- **Interpretação**: Permite visualizar quais partidos têm mais representantes na Câmara
- **Observações**: 
  - As barras são ordenadas por quantidade, do maior para o menor
  - Cada barra representa um partido diferente
  - A altura da barra indica o número de deputados

### 2. Maiores Partidos (Pizza)
- **Arquivo**: `maiores_partidos_pizza.png`
- **Descrição**: Gráfico de pizza mostrando os 5 maiores partidos e agrupando os demais como "Outros"
- **Interpretação**: Facilita a visualização da concentração de poder entre os principais partidos
- **Observações**:
  - Os 5 maiores partidos são mostrados individualmente
  - Todos os outros partidos são agrupados na fatia "Outros"
  - As porcentagens são mostradas em cada fatia

### 3. Distribuição por Estado (Barras)
- **Arquivo**: `deputados_por_estado.png`
- **Descrição**: Gráfico de barras mostrando a quantidade de deputados por estado
- **Interpretação**: Permite visualizar a representatividade de cada estado na Câmara
- **Observações**:
  - As barras são ordenadas por quantidade, do maior para o menor
  - Cada barra representa um estado
  - A altura da barra indica o número de deputados

## Como Interpretar os Resultados

1. **Representatividade por Partido**:
   - Use o gráfico de barras para ver a quantidade exata de deputados por partido
   - Use o gráfico de pizza para entender a proporção dos maiores partidos
   - Observe se há concentração de poder em poucos partidos ou distribuição mais equilibrada

2. **Representatividade por Estado**:
   - Compare a quantidade de deputados com a população de cada estado
   - Observe quais estados têm mais representantes
   - Note que estados mais populosos tendem a ter mais deputados

## Observações Importantes

1. **Limitações dos Dados**:
   - Os dados são limitados às informações básicas dos deputados
   - Não foi possível obter dados de proposições através da API

2. **Atualizações**:
   - Os dados refletem a composição atual da Câmara dos Deputados
   - Para dados mais recentes, execute o script novamente

3. **Interpretação**:
   - Os gráficos são complementares e devem ser analisados em conjunto
   - A representatividade dos estados é definida por lei e leva em conta a população 