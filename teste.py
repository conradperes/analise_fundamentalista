import requests
from datetime import datetime
from pymongo import MongoClient
import matplotlib.pyplot as plt
import pandas as pd
import time

# Função para obter a cotação BTC-USD atual
def get_quotation_btc_usd():
    url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
    response = requests.get(url)
    json_data = response.json()
    
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    rate_float = json_data['bpi']['USD']['rate_float']
    
    result = {
        'date_with_seconds': current_time,
        'btc_usd_rate': rate_float
    }
    
    return result

# Função para salvar a cotação BTC-USD no MongoDB e fazer um plot
def save_quotation_btc_usd():
    try:
        # Conectar ao MongoDB
        client = MongoClient('mongodb://localhost:27017/')
        db = client['quotation']
        collection = db['quotation']
        
        # Obter a cotação atual
        quotation = get_quotation_btc_usd()
        
        # Inserir a cotação no MongoDB
        collection.insert_one({'quotation': quotation})
        
        # Consultar as cotações salvas
        documents = collection.find()
        data = [document['quotation'] for document in documents]
        
        # Criar um DataFrame pandas a partir dos dados
        df = pd.DataFrame(data)
        
        # Fazer o plot do DataFrame
        plt.figure(figsize=(25, 7))  # Definir tamanho maior para a imagem
        plt.plot(df['date_with_seconds'], df['btc_usd_rate'])
        plt.title('Comportamento do BTC-USD nos últimos registros salvos')
        plt.xlabel('Data')
        plt.ylabel('Valor')
        plt.xticks(rotation=45)
        plt.tight_layout()
        # Exibir o plot por 5 segundos
        plt.show()
        time.sleep(5)
        plt.close()
        plt.show(block=False)
        
        print('Cotação salva com sucesso')
    except Exception as e:
        print(f"Erro desconhecido: {e}")
    finally:
        if client:
            client.close()
            print("Conexão com o banco de dados fechada")

def main():
    contador = 0
    while True:
        print(contador, " - Rodando batch de persistência e exibição de comportamento de BTC-USD...")
        save_quotation_btc_usd()
        time.sleep(600)  # Atraso de 600 segundos
        contador += 1

if __name__ == "__main__":
    main()
