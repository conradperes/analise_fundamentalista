from flask import Flask, jsonify, request
import requests
from babel.numbers import format_currency
app = Flask(__name__)

# Chaves API
CMC_API_KEY = '0dfb0915-afa5-4624-99c5-a0d3cb210c53'
CMC_API_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'


def format_brl(value):
    return format_currency(value, 'BRL', locale='pt_BR')
def get_exchange_rate():
    url = "https://api.exchangerate-api.com/v4/latest/USD"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        rate = data["rates"]["BRL"]
        return rate
    else:
        return None
@app.route('/get-crypto-quote', methods=['GET'])
def get_crypto_quote():
    symbol = request.args.get('symbol', 'BTC')  # Padrão para BTC se nenhum símbolo for fornecido

    headers = {
        'X-CMC_PRO_API_KEY': CMC_API_KEY,
        'Accept': 'application/json'
    }

    params = {
        'symbol': symbol
    }

    response = requests.get(CMC_API_URL, headers=headers, params=params)

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({'error': response.json()}), response.status_code


@app.route('/get-crypto-quote-brl', methods=['GET'])
def get_crypto_quote_brl():
    symbol = request.args.get('symbol', 'BTC')  # Padrão para BTC se nenhum símbolo for fornecido

    headers = {
        'X-CMC_PRO_API_KEY': CMC_API_KEY,
        'Accept': 'application/json'
    }

    params = {
        'symbol': symbol
    }

    # Obter o preço em USD
    response = requests.get(CMC_API_URL, headers=headers, params=params)

    if response.status_code != 200:
        return jsonify({'error': response.json()}), response.status_code

    price_usd = response.json()['data'][symbol]['quote']['USD']['price']
    print(f"Price in USD: {price_usd}")  # Imprime o preço em USD no console

    

    exchange_rate = get_exchange_rate()
    print(f"Exchange rate USD to BRL: {exchange_rate}")  # Imprime a taxa de câmbio no console

    # Converter o preço para BRL
    price_brl = price_usd * exchange_rate
    formatted_value = format_brl(price_brl)
    print(f"Price in BRL: {formatted_value}")  # Imprime o preço em BRL no console

    return jsonify({'BTC vale': formatted_value})


if __name__ == '__main__':
    app.run(debug=True)
