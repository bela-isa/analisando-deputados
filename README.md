
# 📊 Análise de Dados — Deputados Federais (Brasil)

Dashboard interativo para análise da composição atual da Câmara dos Deputados, desenvolvido em **Python + Streamlit**, utilizando a **API de Dados Abertos da Câmara dos Deputados**.

O projeto permite explorar, filtrar, visualizar e exportar dados de forma clara, moderna e responsiva, com foco em **análise institucional e transparência pública**.

---

## 🚀 Funcionalidades

### 🔎 Exploração de dados
- Visualização da **distribuição de deputados por partido**
- Visualização da **distribuição de deputados por UF**
- Lista navegável de deputados com busca por nome
- Visualização de detalhes individuais (foto, partido, UF, link oficial)

### 📌 Destaques inteligentes
- **Top 5 partidos** exibidos em cards (resumo visual)
- Quantidade de deputados por partido
- Percentual relativo à base filtrada

### 🎛️ Filtros dinâmicos
- Filtro por **partido**
- Filtro por **estado (UF)**
- Ordenação configurável
- Atualização automática das métricas, gráficos e exportações

### 📤 Exportação de dados
- **CSV com filtros aplicados**
- **CSV da base completa (sem filtros)**
- Exportações separadas e consistentes (sem duplicidade)

### 🧪 Testes automatizados
- Aba dedicada a **testes de sanidade (smoke tests)**
- Verificação automática de:
  - Carregamento de dados
  - Estrutura da base
  - Aplicação de filtros
  - Geração de gráficos
  - Coerência das exportações CSV

---

## 🖥️ Interface

- Design **dark / futurista**
- Detalhes visuais com **neon discreto**
- Layout responsivo (desktop e mobile)
- Componentes organizados por abas
- Performance otimizada com cache configurável

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+**
- **Streamlit**
- **Pandas**
- **Matplotlib**
- **Requests**
- **API Dados Abertos da Câmara**

---

## 📦 Instalação (Local)

### 1️⃣ Clone o repositório
```bash
git clone https://github.com/bela-isa/analisando-deputados.git
cd analisando-deputados
````

### 2️⃣ Crie e ative um ambiente virtual

```bash
python -m venv venv
source venv/bin/activate   # Linux / Mac
# ou
venv\Scripts\activate      # Windows
```

### 3️⃣ Instale as dependências

```bash
pip install -r requirements.txt
```

---

## ▶️ Execução

### Rodar localmente

```bash
streamlit run app.py
```

O aplicativo será iniciado em:

```
http://localhost:8501
```

---

## ☁️ Deploy (Streamlit Cloud)

1. Suba o repositório no GitHub
2. Acesse [https://streamlit.io/cloud](https://streamlit.io/cloud)
3. Crie um novo app apontando para:

   * **Arquivo principal:** `app.py`
4. Defina o Python conforme o `requirements.txt`
5. Deploy automático 🎉

---

## 🧪 Testes Automatizados

Na aba **"Testes"**, é possível rodar verificações automáticas que validam:

* Integridade da base
* Consistência dos filtros
* Funcionamento dos gráficos
* Diferença correta entre CSV filtrado e base completa

Esses testes ajudam a garantir estabilidade antes de deploys ou refatorações.

---

## 📁 Estrutura do Projeto

```
├── app.py                 # Aplicação Streamlit
├── analise_deputados.py   # Script original de análise (offline)
├── ANALISES.md            # Documentação técnica das análises
├── requirements.txt       # Dependências do projeto
└── README.md              # Documentação principal
```

---

## 🌐 Fonte dos Dados

Os dados são obtidos diretamente da API oficial:

🔗 [https://dadosabertos.camara.leg.br/swagger/api.html](https://dadosabertos.camara.leg.br/swagger/api.html)

* Os dados refletem a **composição atual** da Câmara
* Atualização conforme disponibilidade da API

---

## ⚠️ Limitações Conhecidas

* Informações limitadas aos dados públicos disponibilizados
* Não inclui votações, proposições ou histórico legislativo
* Dependência da disponibilidade da API externa

---

## 🤝 Contribuição

Contribuições são bem-vindas!

1. Faça um fork do projeto
2. Crie uma branch para sua feature:

```bash
git checkout -b feature/nova-funcionalidade
```

3. Commit suas alterações:

```bash
git commit -m "Adiciona nova funcionalidade"
```

4. Push para sua branch:

```bash
git push origin feature/nova-funcionalidade
```

5. Abra um Pull Request 🚀

---

