from flask import Flask, jsonify
from datetime import datetime, timedelta
import requests

app = Flask(__name__)

# Função para obter a cotação do BTC-USD a partir da API da CoinGecko
def obter_cotacao_btc_usd():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        'ids': 'bitcoin',
        'vs_currencies': 'usd'
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data['bitcoin']['usd']

# Rota para obter a cotação atual e a variação percentual em relação ao dia anterior
@app.route('/cotacao', methods=['GET'])
def obter_cotacao():
    global cotacao_anterior  # Declara a variável como global

    # Obtém a cotação atual do BTC-USD
    cotacao_atual = obter_cotacao_btc_usd()

    # Calcula a variação percentual em relação ao dia anterior (com base na cotação do dia anterior)
    if 'cotacao_anterior' not in globals():
        cotacao_anterior = obter_cotacao_btc_usd()

    # Obtém a data de ontem
    data_ontem = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

    # Obtém a cotação do BTC-USD do dia anterior
    cotacao_ontem = obter_cotacao_btc_usd()

    # Calcula a variação percentual
    variacao_percentual = ((cotacao_atual - cotacao_ontem) / cotacao_ontem) * 100

    # Atualiza o valor da cotação anterior para a próxima chamada
    cotacao_anterior = cotacao_atual

    # Obtém o timestamp atual com precisão de segundos
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Retorna a cotação atual, a variação percentual e o timestamp como resposta JSON
    resposta = {
        'cotacao_atual': cotacao_atual,
        'variacao_percentual': round(variacao_percentual, 2),
        'timestamp': timestamp
    }

    return jsonify(resposta)

if __name__ == '__main__':
    app.run(debug=True)
