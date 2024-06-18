# Desafio de Ciência de Dados

## Introdução
Esse projeto foi desenvolvido para o desafio de ciência de dados proposto pela Makasi. O desafio consiste em prever o orçamento de um projeto de construção civil com base em algumas variáveis. O objetivo é realizar predições de orçamento com base em dados de projetos anteriores, além de analises úteis.

## Arquivos 
Os arquivos disponíveis para esse desafio são:
#### Dados
- 'amostra_projeto1.csv'
- 'amostra_projeto_2.csv'
- 'amostra_projeto_3.csv'
- 'projeto_4.csv'
- 'amostras_projetos.xlsx'

#### Documentação
A documentação de CLASSES e FUNÇÕES está disponível na pasta _docs/_.

#### Requirements
O arquivo requirements.txt contém as dependências necessárias para rodar o projeto.

#### Códigos e Scripts
- main.ipynb - Contém o código do projeto, desde a importação dos dados até a análise de dados e criação do modelo de machine learning.
- script.py - Contém o código de execução do Modelo de predição do projeto 3 e 4.
- utils/ - Contém os códigos de funções auxiliares para a execução do projeto. 

#### Usage
Inicialmente clone o repositório:
```bash
git clone https://github.com/vector-b/makasi-data
```

Instale as dependências necessárias:
```bash
pip install -r requirements.txt
```

Para executar o script do modelo:
```bash
python script.py
```

O arquivo main.ipynb será executado no Jupyter Notebook.


## Análise de Dados
**AVISO IMPORTANTÍSSIMO:** <br>
O conjunto de dados utilizado é extremamente pequeno e pode não ser representativo de um problema real. A análise de dados e o modelo de machine learning foram criados com base nesses dados, e não necessariamente refletem a realidade. O objetivo é mostrar o processo de análise de dados e machine learning, e não necessariamente criar um modelo preciso.

A documentação de CLASSES e FUNÇÕES está disponível na pasta docs.

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

Para trabalharmos com ambos os DataFrames, foi criado um dicionário de DataFrames, onde cada chave é o nome do projeto e o valor é um dicionário contendo o DataFrame do cabeçalho, a transposta do DataFrame do cabeçalho e o DataFrame de orçamento.

A estrutura do dicionário é a seguinte:
```python
{
    'amostra_projeto1': {
        'header': DataFrame,
        'budget': DataFrame,
        'header_T: DataFrame.T
    },
    'amostra_projeto2': {
        'header': DataFrame,
        'budget': DataFrame,
        'header_T: DataFrame.T
    },
    'amostra_projeto3': {
        'header': DataFrame,
        'budget': DataFrame,
        'header_T: DataFrame.T
    },
    'projeto_4': {
        'header': DataFrame,
        'header_T: DataFrame.T
    }
}
```

### Exploração inicial dos dados
Após a importação dos dados, foi realizada uma exploração inicial dos dados. Foram verificados os tipos de dados, a presença de valores nulos, cabeçalhos e outras informações relevantes para a análise.

- Valores nulos: Os valores nulos são apropriados para esse problema. A presença de valores nulos pode indicar que o item não é de fato um objeto físico, mas sim um serviço ou etapa do projeto, é interessante checar os valores de Execução e Material, porém sempre haverá um valor total para cada entrada.

- Tipos de dados: Após o processamento dos dados, os tipos de dados foram ajustados para os tipos corretos. Os valores numéricos foram convertidos para float, e os valores monetários foram convertidos para float.

- Outliers: Não foram identificados outliers nos dados.

- Colinearidade: Há uma certa colinearidade entre algumas variáveis, como a quantidade de banheiros e a área construída. A quantidade de banheiros possui uma correlação positiva com o orçamento total do projeto. Quanto mais banheiros, maior o orçamento e área. Com isso, foi criada uma nova variável que é a razão entre a quantidade de banheiros e a área construída, que possui uma correlação positiva com o orçamento total do projeto.



### Insights obtidos

Primeiramente, ao juntar as tabelas de sumário do projeto e de orçamento, foi possível identificar algumas relações entre as variáveis.
A correlação entre as variáveis foi calculada e foi possível identificar algumas relações interessantes:

![Matriz de correlação](src/imgs/corr_simplified.png)

Nessa matriz simplificada podemos observar que:
- A quantidade de banheiros (BWCs) possui uma correlação positiva com o orçamento total do projeto. Quanto mais banheiros, maior o orçamento e área. Com isso, foi criada uma nova variável que é a razão entre a quantidade de banheiros e a área construída, que possui uma correlação positiva com o orçamento total do projeto.

- A área do terreno tem uma correlação média positiva com a área construída, o que nos leva a entender que não necessariamnte por se haver mais espaço terá mais construção. Possuindo mais dados de tipologia, poderíamos entender melhor essa relação entre espaço livre e construído.

Para trabalharmos com as categorias únicas de orçamento no dataset e entendermos melhor a relação entre elas e as variáveis do projeto, foi necessário juntarmos as duas tabelas, header e orçamento, e agregarmos os valores de orçamento por categoria única. Com isso, foi possível criar uma matriz de correlação extendida, que nos dá uma visão mais ampla das relações entre as variáveis.
   
![Correlação Extentida](src/imgs/corr_extended.png)

Essa é matriz de correlação contendo as _Categorias Únicas e seu total de orçamento_. 

## Predições e Machine Learning
Nesse projeto a utilização de técnicas de machine learning e métodos estatísticos mais avançados foi um tanto limitada devido a quantidade de dados, afinal com apenas 3 projetos completos e 1 incompleto, não é possível criar um modelo de machine learning que generalize bem para novos dados. Além disso, até métricas de avaliação de modelos como o R² e RMSE não seriam confiáveis com tão poucos dados.

Porém, foi possível criar um modelo de regressão linear simples para prever o orçamento total do projeto com base em algumas variáveis. O modelo foi treinado com os dados dos projetos 1, 2 e 3, e testado com os dados do projeto 4.

### Variáveis utilizadas
As variáveis utilizadas para a previsão do orçamento total do projeto foram:
    - Tipologia
    - Área Construída
    - Área Terreno
    - Área Fachada
    - Área Parede
    - Valor Total 

### Encoding e Normalização
Para a utilização das variáveis categóricas, foi necessário realizar o encoding das variáveis categóricas. Foi utilizado o método de _One Hot Encoding_ para a variável _Tipologia_.

As variáveis numéricas foram normalizadas utilizando o método _MinMaxScaler_.

### Treinamento do modelo
O modelo utilizado foi um modelo de regressão linear múltipla.
Esse modelo segue o seguinte formato:
    y = b0 + b1*x1 + b2*x2 + ... + bn*xn
Que pode ser escrito de forma matricial:
    y = X * b

O modelo foi importado da biblioteca _sklearn_ correspondendo a classe _LinearRegression_.
Como temos poucos dados, foi utilizado o método de Leave One Out Cross Validation para treinar o modelo. O modelo foi treinado com os dados dos projetos 1, 2 e testado com o projeto 3. 

No caso da predição do projeto 4, o modelo foi treinado com os dados dos projetos 1, 2 e 3, e testado com o projeto 4.

### Resultados
Podemos separar os resultados por diferentes metodologias de treino e teste.
#### Leave One Out Cross Validation
Leave One Out Cross Validation é um método de validação cruzada que consiste em treinar o modelo com todos os dados, exceto um, e testar o modelo com o dado que foi excluído. Esse processo é repetido para todos os dados.
##### Resultados
| Target | split_index | MSE | MAE | RMSE |
|---|---|---|---|---|
| total_execution_cost | 0 | 7.183527e+09 | 84755.69 | 84755.69 |
| total_execution_cost | 1 | 1.071489e+11 | 327336.03 | 327336.03 |
| total_execution_cost | 2 | 1.669600e+11 | 408607.34 | 408607.34 |
| total_material_cost | 0 | 1.562918e+11 | 395337.63 | 395337.63 |
| total_material_cost | 1 | 5.560229e+11 | 745669.44 | 745669.44 |
| total_material_cost | 2 | 1.416731e+12 | 1190264.94 | 1190264.94 |
| total_cost | 0 | 2.304896e+11 | 480093.31 | 480093.31 |
| total_cost | 1 | 1.151341e+12 | 1073005.48 | 1073005.48 |
| total_cost | 2 | 2.556393e+12 | 1598872.28 | 1598872.28 |

#### Predição do Projeto 4
Para a predição do projeto 4, o modelo foi treinado com os dados dos projetos 1, 2 e 3, e testado com o projeto 4.
##### Resultados
| Column | Value |
|---|---|
| total_execution_cost | 1325055.01 |
| total_material_cost | 2687063.71 |
| total_cost | 4012118.72 |


## Conclusão
### Resultados
Com esse experimento, foi possível criar um modelo de regressão linear simples para prever o orçamento total do projeto com base em algumas variáveis. Todavia, é importante ressaltar que o modelo não é preciso e não generaliza bem para novos dados. A quantidade de dados é muito pequena e não é possível criar um modelo confiável com tão poucos dados.

Com os insights obtidos, foi possível identificar algumas relações entre as variáveis e o orçamento total do projeto. A quantidade de banheiros possui uma correlação positiva com o orçamento total do projeto. Quanto mais banheiros, maior o orçamento e área. A área do terreno tem uma correlação média positiva com a área construída, o que nos leva a entender que não necessariamnte por se haver mais espaço disponível haveram maiores construções, apesar de que espaço construiído sempre será menor que o espaço disponível (essa correlação sempre será positiva).

Mais dados seriam úteis para entender melhor essas relações e também criar um modelo mais preciso.

### Respostas ao Desafio
- A estimativa de custo para o "projeto 4" foi de R$ 4.012.118,72.
- A documentação tanto do método usado para chegar ao valor previsto para o "Projeto 4", quanto das etapas e ferramentas usadas no processo estão descritas neste mesmo documento, mais informações sobre as classes e funções utilizadas estão disponíveis na pasta docs.
- O nível de acuracidade da estimativa é baixo, devido a quantidade de dados disponíveis. O modelo não generaliza bem para novos dados e não é preciso. Porém as melhores métricas obtidas foram, com base no RMSE (Root Mean Squared Error), que significa a raiz do erro quadrático médio, que é uma medida de dispersão dos dados:
    - RMSE total_execution_cost: 327336.03
    - RMSE total_material_cost: 395337.63
    - RMSE total_cost: 480093.31

    Ou seja, o modelo tem um erro médio de R$ 327.336,03 para o custo total de execução, R$ 395.337,63 para o custo total de material e R$ 480.093,31 para o custo total do projeto.
- O risco implícito nessa previsão é alto, devido a quantidade de dados disponíveis. Recomenda-se a coleta de mais dados para criar um modelo mais preciso e ter métricas mais confiáveis. E realizar predições baseadas apenas nas colunas do cabeçalho do projeto, como foi feito nesse experimento, talvez não seja a melhor abordagem.
