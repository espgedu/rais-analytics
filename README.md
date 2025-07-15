# Análise de Dados RAIS — Diversidade, Salários e Liderança

Este projeto realiza uma análise exploratória dos dados da **RAIS (Relação Anual de Informações Sociais)** da região sudeste, com foco em:

- Diversidade racial e de gênero  
- Distribuição de salários  
- Cargos e posições de liderança  

Utilizei os microdados dos anos **2010** e **2024**, aplicando ferramentas de **Python** e **SQL** para gerar insights sobre o mercado de trabalho brasileiro.

---

## Fonte dos Dados

Os dados utilizados estão disponíveis publicamente no portal do governo federal:

[Microdados RAIS e CAGED — Gov.br](https://www.gov.br/trabalho-e-emprego/pt-br/assuntos/estatisticas-trabalho/microdados-rais-e-caged)

---

## Estrutura do Projeto

analysis/sql_queries

data/
├── raw/ # Arquivos brutos da RAIS
├── processed/ # Dados tratados prontos para análise

src/
└── etl/ # Scripts de extração e transformação de dados

**Observação:** O processo de ETL foi parcialmente automatizado, o carregamento dos dados (`Load`) foi feito de forma manual, sendo armazenados localmente para um banco **PostgreSQL**.

