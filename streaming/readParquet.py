import pandas as pd

def read_parquet_to_pandas(parquet_file):
    # Ler o arquivo Parquet para um DataFrame do Pandas
    df = pd.read_parquet(parquet_file)
    return df

def main():
    # Nome do arquivo Parquet (altere conforme necessário)
    CCCCCCCCCCCCCCCCCCCCCCCCCCC

    # Ler o arquivo Parquet
    df = read_parquet_to_pandas(parquet_file)

    # Imprimir o DataFrame
    print("Conteúdo do DataFrame:")
    print(df)

if __name__ == "__main__":
    main()
