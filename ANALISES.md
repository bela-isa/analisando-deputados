# 📊 Análises de Dados — Deputados Federais

Este documento descreve as análises realizadas a partir dos dados dos Deputados Federais brasileiros, bem como a forma correta de interpretar os resultados exibidos no dashboard interativo desenvolvido com **Streamlit**.

As análises utilizam dados públicos obtidos por meio da **API de Dados Abertos da Câmara dos Deputados** e refletem a composição atual da Câmara.

---

## 📁 Bases de Dados Utilizadas

Os dados são carregados diretamente da API oficial e tratados em memória para visualização e exportação.

### Estrutura principal da base
Cada deputado contém, entre outras, as seguintes informações:
- Nome parlamentar
- Partido (sigla)
- Unidade Federativa (UF)
- Foto oficial
- Identificador único (ID)
- Link para o registro oficial na API

---

## 📤 Exportações Disponíveis

O dashboard permite exportar dados em dois contextos distintos:

### 1️⃣ CSV com filtros aplicados
- Contém **apenas os deputados visíveis após a aplicação dos filtros**
- Ideal para análises direcionadas (por partido, estado, etc.)
- Reflete exatamente o que está sendo exibido na interface

### 2️⃣ CSV da base completa (sem filtros)
- Contém **todos os deputados carregados da API**
- Independe de filtros ativos
- Útil como base bruta para análises externas

> ⚠️ Importante: os dois arquivos **não são iguais** e atendem a objetivos analíticos diferentes.

---

## 📈 Análises e Visualizações

### 1. Distribuição de Deputados por Partido
- **Formato**: Gráfico de barras horizontais
- **Objetivo**: Mostrar a quantidade de deputados por partido
- **Interpretação**:
  - Barras maiores indicam partidos com maior representação
  - Ordenação decrescente facilita a comparação direta
- **Uso prático**:
  - Identificar partidos majoritários
  - Avaliar concentração ou fragmentação partidária

---

### 2. Distribuição de Deputados por Unidade Federativa (UF)
- **Formato**: Gráfico de barras horizontais
- **Objetivo**: Exibir a quantidade de deputados por estado
- **Interpretação**:
  - Estados com maior população tendem a ter mais representantes
  - A visualização facilita comparações rápidas entre UFs
- **Observação**:
  - A distribuição segue critérios legais definidos pela Constituição

---

### 3. Destaques — Top 5 Partidos
- **Formato**: Cards de destaque (quadrados com bordas arredondadas)
- **Conteúdo exibido**:
  - Sigla do partido
  - Quantidade de deputados
  - Percentual relativo à base atual (com filtros)
  - Ranking (Top 1, Top 2, etc.)

#### Por que usar cards em vez de gráfico?
- Evita redundância visual
- Facilita leitura rápida
- Mantém consistência com o restante do dashboard
- Reduz ruído visual em telas menores

Esses destaques funcionam como um **resumo executivo** da composição partidária.

---

## 🧪 Testes Automatizados (Sanidade)

O projeto inclui uma aba dedicada a **testes automatizados**, com foco em verificação funcional do dashboard.

### Testes realizados:
- Carregamento correto da base de dados
- Estrutura mínima esperada do DataFrame
- Funcionamento dos filtros (partido e UF)
- Coerência entre dados filtrados e exportações
- Geração correta das visualizações

Esses testes ajudam a garantir:
- Estabilidade do app
- Confiança antes de deploys
- Facilidade de manutenção e refatoração

---

## 🧠 Como Interpretar os Resultados

### Representatividade por Partido
- Utilize o gráfico de barras para valores absolutos
- Utilize os cards de destaque para leitura rápida
- Compare percentuais considerando os filtros ativos

### Representatividade por Estado
- Compare estados entre si
- Lembre-se que a distribuição é legalmente definida
- Evite comparações diretas sem considerar população

---

## ⚠️ Observações Importantes

1. **Limitações dos dados**
   - Apenas dados públicos básicos estão disponíveis
   - Não inclui votações, proposições ou histórico legislativo

2. **Atualização dos dados**
   - Os dados refletem o estado atual da API
   - Para atualizar, basta recarregar o app ou limpar o cache

3. **Uso responsável**
   - As análises são descritivas
   - Não representam posicionamentos políticos ou juízos de valor

---

## 🌐 Fonte dos Dados

API de Dados Abertos da Câmara dos Deputados  
🔗 https://dadosabertos.camara.leg.br/swagger/api.html
