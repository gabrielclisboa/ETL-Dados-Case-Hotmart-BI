# Documentação do Projeto ETL

## Descrição
Este projeto foi desenvolvido utilizando Python 3.12 e consiste em um processo ETL (Extração, Transformação e Carga) de dados de vendas em formato CSV. O ETL é realizado em Python, utilizando a biblioteca Pandas para manipulação de dados, Faker para geração de dados fictícios e os módulos padrão `os` e `random`.

## Estrutura do Projeto
O projeto é composto por cinco arquivos principais:

1. `pipeline.py`: Contém o código do pipeline ETL, incluindo as funções de extração, transformação, carregamento e a função principal `run_pipeline()`.

2. `data/`: Arquivo CSV, contendo os dados brutos de vendas, deve ser inserido nessa pasta.

3. `result/`: Diretório de saída para armazenar os resultados do ETL.

4. `README.md`: Documentação do projeto em formato Markdown.

# Dependências do Projeto

As dependências do projeto podem ser instaladas seguindo os passos abaixo:

1. **Python (versão 3.12):**
   - [Download Python 3.12](https://www.python.org/downloads/release/python-312/)
   - Execute o instalador baixado.

2. **Pandas:**
   - Abra o terminal ou prompt de comando.
   - Navegue até a pasta raiz do projeto.
   - Execute o seguinte comando:
     ```bash
     pip install pandas
     ```

3. **Faker:**
   - No mesmo terminal ou prompt de comando e na mesma pasta do projeto, execute:
     ```bash
     pip install faker
     ```

Certifique-se de estar na pasta correta antes de executar os comandos `pip`.

## Execução do Projeto

1. **Adicionar arquivo CSV de vendas ao projeto :**
2. 
    -Adicione o arquivo `sales_data_202309132316.csv` na pasta `result/`

3. **Executar o projeto:**

    - Para executar o projeto, basta rodar o script `pipeline.py`:
    ```bash
    python pipeline.py
    ```
O script realizará a extração dos dados, transformação conforme regras definidas, e salvará os resultados na pasta `result/`.

## Estrutura do Código
### Funções Principais
- `extract(file_path: str) -> DataFrame`: Extrai os dados do arquivo CSV e retorna um DataFrame Pandas.

- `transform(df: DataFrame) -> Tuple[DataFrame, DataFrame, DataFrame, DataFrame, DataFrame]`: Realiza a transformação dos dados brutos em cinco DataFrames distintos: Dimensão Afiliado, Dimensão Produtor, Fato Venda, Dimensão Comprador e Dimensão Segmento do Usuário.

- `load(df: DataFrame, save_path: str)`: Salva um DataFrame em um arquivo CSV no caminho especificado.

- `run_pipeline()`: Função principal que executa o pipeline ETL completo.

### Estrutura do Console Log
As mensagens do console são formatadas em caixas delimitadas por traços, destacando cada etapa do processo ETL.

## Notas Adicionais
- A geração de dados fictícios é realizada utilizando a biblioteca Faker para criar nomes, endereços e e-mails fictícios.

- Os resultados do ETL são salvos na pasta `result/` em arquivos CSV separados para cada tabela.

- O ETL pode durar até 1-2 minutos, por conta da geração dos dados fake.

Caso haja dúvidas, estou a disposição para saná-las.
