# Inteligência de Dados como Ferramenta de Apoio à Gestão — Programa Elas++ (PUC Minas)

Este repositório contém a infraestrutura de Dados desenvolvida para o ecossistema de Business Intelligence (BI) do **Programa Elas++**, um projeto de extensão social da **PUC Minas**.

O objetivo central desse sistema é centralizar, tratar e modelar dados extraídos de planilhas de feedbacks e formulários de oficinas. A solução permite a análise estratégica do engajamento e do impacto do programa no incentivo a carreiras nas áreas de **STEM** (Ciência, Tecnologia, Engenharia e Matemática).

---

## Arquitetura e Fluxo de Dados (ETL)

O projeto foi desenhado seguindo práticas de Data Warehousing para estruturar dados brutos dispersos em um banco de dados analítico PostgreSQL, hospedado em nuvem via Railway.

1. **Extração (E):** Consumo automatizado de planilhas de registros e formulários de satisfação das oficinas.
2. **Transformação (T):** Limpeza, padronização de tipos de dados, consistência de campos textuais e cálculo de métricas de engajamento.
3. **Carga (L):** Povoamento das tabelas estruturadas no banco analítico.

---

## Modelagem de Dados

Para otimizar a performance das consultas que alimentam a camada de apresentação, os dados foram organizados utilizando o conceito de modelagem dimensional em **Esquema Estrela (Star Schema)**. 

Essa abordagem divide as informações entre tabelas de dimensões (contendo os contextos e perfis, como dados do participante, elementos de tempo e categorias dos eventos) e tabelas fato (contendo as métricas de atividades, volumetria e indicadores de desempenho calculados).

---

## Requisitos de Negócio Cobertos pelo Dashboard

O modelo de dados fornece os insumos analíticos necessários para responder aos seguintes requisitos estratégicos da coordenação do programa:

1. **Impacto em STEM:** Mensurar o impacto direto da oficina na intenção da participante em seguir carreira nas áreas de STEM.
2. **Efetividade e Satisfação:** Avaliar a efetividade técnica e pedagógica das oficinas com base na satisfação geral e aplicabilidade prática do conhecimento.
3. **Fatores de Recomendação:** Analisar quais fatores mais influenciam a nota de recomendação do projeto.
4. **Perfis de Engajamento:** Identificar perfis demográficos (idade e ano do ensino médio) com maiores taxas de engajamento e retenção.
5. **Intenção Feminina em STEM:** Calcular o percentual específico de meninas com intenção declarada de seguir na área de STEM.
6. **Disparidade de Gênero:** Apresentar a relação percentual entre meninos e meninas que pretendem seguir carreiras tecnológicas.
7. **Evolução Volumétrica:** Monitorar a evolução histórica do número de participantes das oficinas ao longo do tempo.
8. **Análise de Atividades:** Comparar a aderência e o engajamento entre os diferentes tipos de atividades e temas oferecidos.

---

## Como Instalar e Executar o Projeto

### Pré-requisitos

Certifique-se de que você tem instalado na sua máquina:

- [Python 3.13+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)
- Acesso a um banco de dados **PostgreSQL** (local ou em nuvem, ex.: Railway)
- Credenciais de acesso ao **SharePoint** da organização (para extração automática dos dados)

---

### 1. Clonar o repositório

```bash
git clone https://github.com/ICEI-PUC-Minas-PMV-SI/ellas.git
cd ellas
```

---

### 2. Criar e ativar o ambiente virtual

**Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

---

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

---

### 4. Configurar as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com base no modelo abaixo:

```env
# Banco de dados PostgreSQL
POSTGRES_HOST=seu_host
POSTGRES_PORT=5432
POSTGRES_DB=nome_do_banco
POSTGRES_USER=seu_usuario
POSTGRES_PASSWORD=sua_senha

# SharePoint (para extração automática das planilhas)
SHAREPOINT_URL=https://suaorganizacao.sharepoint.com/sites/seu-site
SHAREPOINT_TENANT=id-do-tenant-azure
SHAREPOINT_CLIENT_ID=id-do-app-azure
SHAREPOINT_USER=seu_email@organizacao.com
SHAREPOINT_PASS=sua_senha
FILE_PATH=/sites/seu-site/Documentos/nome-da-planilha.xlsx
```

> **Atenção:** Nunca versione o arquivo `.env`. Ele já deve estar listado no `.gitignore`.

---

### 5. Executar o pipeline ETL

```bash
python src/main.py
```

O script irá:
1. Autenticar no SharePoint e baixar a planilha de formulários
2. Realizar as transformações e limpeza dos dados
3. Carregar as tabelas dimensionais e fato no banco PostgreSQL configurado

---

### Alternativa: Execução via Docker

Se preferir rodar em container sem configurar o ambiente Python localmente:

```bash
# Construir a imagem
docker build -t ellas-etl .

# Executar passando as variáveis de ambiente
docker run --env-file .env ellas-etl
```

---

## Diagrama do Projeto & Wireframe Interativo

- https://github.com/ICEI-PUC-Minas-PMV-SI/ellas/blob/50b0be4cfd245739a435dceeb7cc06d617eb2804/docs/ellas%2B%2B-der.png
- https://github.com/ICEI-PUC-Minas-PMV-SI/ellas/blob/50b0be4cfd245739a435dceeb7cc06d617eb2804/docs/Elas%20%2B%2B%20-%20Projeto%20de%20Extens%C3%A3o.html
