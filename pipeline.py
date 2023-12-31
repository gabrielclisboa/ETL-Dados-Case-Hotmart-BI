import pandas as pd
import random
import os
from pandas.core.frame import DataFrame
from faker import Faker

def extract(file_path: str) -> DataFrame:
    '''
    extracts csv data and converts to pandas DataFrame

    args:
        file_path (str): path to the csv file
    
    returns:
        df (DataFrame): pandas dataframe containing the csv data
    '''

    # extracts the csv data as pandas dataframe 
    print("Iniciando extração dos dados...")

    df = pd.read_csv(file_path)

    print("Extração executada com sucesso!")

    return df

def transform(df: DataFrame) -> DataFrame:
    '''
    cleans data and transforms it into the desired format

    args:
        df (DataFrame): pandas dataframe containing the raw data
    
    returns:
        df (DataFrame): pandas dataframe containing the clean data
    '''

    print("Iniciando transformação dos dados...")

    fake = Faker('pt_BR') 

    # Transformação para a Tabela Dimensão Produtor Afiliado

    # Z-score
    df['purchase_value'] = df['purchase_value'].apply(lambda x: x if x >= 0 else -1 * x)
    df['purchase_value'] = round(df['purchase_value'] * 100 + 60, 2)


    dim_afiliado = df[['affiliate_id']].drop_duplicates()
    dim_afiliado['name'] = dim_afiliado['affiliate_id'].apply(lambda x: fake.name())
    dim_afiliado['sales_history'] = df.groupby('affiliate_id').size().reindex(dim_afiliado['affiliate_id']).fillna(0).astype(int).values
    dim_afiliado['creation_date'] = dim_afiliado['affiliate_id'].apply(lambda x:pd.to_datetime (fake.date_time_between(start_date='-10y', end_date='-7y')))
    dim_afiliado['status'] = True
    dim_afiliado['email'] = dim_afiliado['affiliate_id'].apply(lambda x: fake.email())


    # Transformação para a Tabela Dimensão Produtor

    # Filtrar vendas onde affiliate_id é igual a producer_id
    vendas_do_produtor = df[df['affiliate_id'] == df['producer_id']]
 
    dim_produtor = df[['producer_id']].drop_duplicates()
    dim_produtor['name'] = dim_produtor['producer_id'].apply(lambda x: fake.name()) 
    dim_produtor['address'] = dim_produtor['producer_id'].apply(lambda x: fake.address().replace('\n', ' ').strip());  
    dim_produtor['email'] = dim_produtor['producer_id'].apply(lambda x: fake.email())
    dim_produtor['sales_history'] = vendas_do_produtor['producer_id'].value_counts().reindex(dim_produtor['producer_id']).fillna(0).astype(int).values
    dim_produtor['status'] = True
    dim_produtor['creation_date'] = dim_produtor['producer_id'].apply(lambda x: pd.to_datetime (fake.date_time_between(start_date='-10y', end_date='-7y')))
    dim_produtor['rating'] = dim_produtor['producer_id'].apply(lambda x: round(random.uniform(0, 5), 1))

    # Transformação para a Tabela Fato Venda
    fato_venda = df[[
        'purchase_id', 'product_id', 'affiliate_id', 'producer_id', 'buyer_id',
        'purchase_date', 'product_creation_date', 'product_category', 'product_niche',
        'purchase_value', 'affiliate_commission_percentual', 'purchase_device',
        'purchase_origin', 'is_origin_page_social_network', 'Venda'
    ]]

    # Transformação para a Tabela Dimensão Comprador
    dim_comprador = df[['buyer_id']].drop_duplicates()
    dim_comprador['name'] = dim_comprador['buyer_id'].apply(lambda x: fake.name()) 
    dim_comprador['address'] = dim_comprador['buyer_id'].apply(lambda x:  fake.address().replace('\n', ' ').strip())  
    dim_comprador['email'] = dim_comprador['buyer_id'].apply(lambda x: fake.email())
    dim_comprador['age'] = dim_comprador['buyer_id'].apply(lambda x: random.randint(18, 70)) 
    dim_comprador['status'] = True  
    dim_comprador['creation_date'] = dim_comprador['buyer_id'].apply(lambda x: pd.to_datetime (fake.date_time_between(start_date='-10y', end_date='-7y')))

    # Transformação para a Tabela Dimensão Segmento do Usuário
    dim_segmento_usuario = pd.DataFrame(index=df.index)  
    dim_segmento_usuario['user_segment_id'] = df.index + 1
    dim_segmento_usuario['category_name'] = ''  
    dim_segmento_usuario['date_sale'] = dim_segmento_usuario['user_segment_id'].apply(lambda x: pd.to_datetime (fake.date_time_between(start_date='-10y', end_date='-7y'))) 
    dim_segmento_usuario['last_category'] = 0  
    dim_segmento_usuario['current_category'] = ''


    print("Transformação dos dados executada com sucesso!")  

    # Retornar os DataFrames transformados
    return dim_afiliado, dim_produtor, fato_venda, dim_comprador, dim_segmento_usuario

def load(df: DataFrame, save_path: str):
    '''
    writes pandas DataFrame to csv file

    args:
        df (DataFrame): pandas dataframe containing the clean data
        save_path (str): path to save the csv file
    
    returns:
        None
    '''

    df.to_csv(save_path, index=False)
    print(f'DataFrame saved to {save_path}')



def run_pipeline():

    file_path = os.getcwd()+"/data/sales_data_202309132316.csv"
    result_path = os.getcwd()+"/result/"

    # Carrega os dados
    df = extract(file_path)

    # Realiza as transformações
    dim_afiliado, dim_produtor, fato_venda, dim_comprador, dim_segmento_usuario = transform(df)

    # Salva os resultados na pasta 'result'
    print("Iniciando carregamento dos dados...")

    os.makedirs(result_path, exist_ok=True)
    load(dim_afiliado, result_path+"dim_afiliado.csv")
    load(dim_produtor, result_path+"dim_produtor.csv")
    load(fato_venda, result_path+"fato_venda.csv")
    load(dim_comprador,result_path+"dim_comprador.csv")
    load(dim_segmento_usuario,result_path+"dim_segmento_usuario.csv")

    print("Carregamento dos dados executado com sucesso!")
    print("ETL finalizado.")


if __name__ == "__main__":
    # run pipeline

    print("Iniciando ETL...")

    run_pipeline()