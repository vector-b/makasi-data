# Desafio de Ciência de Dados

## Introdução
- Objetivo do desafio
- Contexto do problema
- Importância da análise de dados

## Análise de Dados

### Arquivos disponíveis
Foram disponibilizados 4 arquivos, sendo 4 csv e 1 xlsx. Os arquivos foram importados para o ambiente de desenvolvimento e carregados em DataFrames. Os arquivos mencionados são:
- 'amostra_projeto1.csv'
- 'amostra_projeto_2.csv'
- 'amostra_projeto_3.csv'
- 'projeto_4.csv'
- 'amostras_projetos.xlsx'

#### Estrutura
O arquivo .xlsx é um arquivo Excel que contém 4 planilhas, que correspondem aos arquivos csv mencionados acima. Cada planilha contém informações sobre um projeto específico.

Cada arquivo possui 2 tabelas, sendo uma um sumário do projeto e a outra uma tabela de orçamento dos itens do projeto. Com exceção do arquivo 'projeto_4.csv', que possui apenas o cabeçalho do projeto (header), afinal um dos objetivos é prever o orçamento dos itens do projeto.

Exemplo de tabela de sumário do projeto:

|       INFO       |       VALOR        |
|--------------------|--------------------|
| Titulo             | Projeto 1 - Wa     |
| Tipologia          | Térrea             |
| Área Terreno       | 485.00             |
| Área Construída    | 246.63             |
| Área Fundação      | 237.98             |
| Área Fachada       | 597.88             |
| Área Parede        | 615.86             |
| Qtde BWCs          | 5.00               |

Exemplo de tabela de orçamento do projeto:

| Item | Referência      | Tipo       | Código            | Descrição              | Unid. | Quantidade | BDI  | Preço Material | Preço Execução | Preço Unitário | Preço Total |
|------|-----------------|------------|-------------------|------------------------|-------|------------|------|----------------|----------------|----------------|-------------|
| 1.   |                 |            |                   | ETAPAS PRE OBRA        |       |            | 0.0% |                |                |                | $9,286.25   |
| 1.1. |                 |            |                   | SONDAGEM               |       |            | 0.0% |                |                |                | $3,000.00   |
| 1.1.1| MKS_COMPOSICOES | COMPOSICAO | CMP_INF-SON       | SONDAGEM               | VB    | 1          | 0.0% |                | $3,000.00      | $3,000.00      | $3,000.00   |
| 1.2. |                 |            |                   | LEVANTAMENTO TOPOGRAFICO|       |            | 0.0% |                |                |                | $2,400.00   |
| 1.2.1| MKS_COMPOSICOES | COMPOSICAO | CMP_INF-LVT       | LEVANTAMENTO TOPOGRAFICO| VB    | 2          | 0.0% |                | $1,200.00      | $1,200.00      | $2,400.00   |
| 1.3. |                 |            |                   | RESPONSABILIDADE TECNICA|       |            | 0.0% |                |                |                | $177.56     |
| 1.3.1| MKS_COMPOSICOES | COMPOSICAO | CMP_EPO-TAX-ART   | TAXA ART               | VB    | 2          | 0.0% |                | $88.78         | $88.78         | $177.56     |
| 1.4. |                 |            |                   | TAXAS DE APROVACAO     |       |            | 0.0% |                |                |                | $3,708.69   |
| ...  | ...             | ...        | ...               | ...                    | ...   | ...        | ...  | ...            | ...            | ...            | ...         |


### Pré-processamento dos dados
O primeiro passo foi realizar a leitura e importação dos dados. Como possuímos 2 tabelas em cada arquivo .csv (com exceçãoo do projeto 4), foi necessário ler cada tabela separadamente e armaezá-las em DataFrames distintos. Foi criado um dicionário de DataFrames para armazenar os DataFrames de cada arquivo e suas respectivas tabelas.

Alguns dados tiveram a necessidade de serem tratados, como a remoção de caracteres especiais, conversão de tipos de dados, e outros.

Alguns valores numéricos e monetários estavam como strings, foi necessário realizar a conversão para float. Exemplos:
    
-   4,00 (object) -> 4.00 (float)
-   $4,000.00 (object) -> 4000.00 (float)

    
Consulte a seção "Estruturas e Dataframes" para mais detalhes sobre a estrutura do dicionário.

### Exploração inicial dos dados
Após a importação dos dados, foi realizada uma exploração inicial dos dados. Foram verificados os tipos de dados, a presença de valores nulos, cabeçalhos e outras informações relevantes para a análise.

- Valores nulos: Os valores nulos são apropriados para esse problema. A presença de valores nulos pode indicar que o item não é de fato um objeto físico, mas sim um serviço ou etapa do projeto, é interessante checar os valores de Execução e Material, porém sempre haverá um valor total para cada item.

- Tipos de dados: Os tipos de dados foram verificados e estão coerentes com o esperado. Os valores numéricos estão como float e int, e as strings estão como object.


   





- Pré-processamento dos dados
- Exploração inicial dos dados
- Insights obtidos

## Manipulação de Tabelas
- Transformação e limpeza dos dados
- Criação de novas variáveis
- Agregação e sumarização dos dados

## Machine Learning
- Preparação dos dados para treinamento
- Escolha do algoritmo de machine learning
- Treinamento do modelo
- Avaliação do modelo
- Insights obtidos com o modelo

## Conclusão
- Recapitulação dos principais pontos
- Resultados alcançados
- Lições aprendidas
- Próximos passos

## Referências
- Links para recursos utilizados
- Referências bibliográficas
