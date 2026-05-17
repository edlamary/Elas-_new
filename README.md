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

