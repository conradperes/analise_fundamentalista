import requests
import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from influxdb_client import InfluxDBClient, Point, WritePrecision, WriteOptions
from datetime import datetime
import time

# Configurações do InfluxDB
INFLUXDB_URL = "http://localhost:8086"
INFLUXDB_TOKEN = "ZljL7bCRd7aOfOdbAbMer5RNHIOFjOYi4BosubGfKmSWq2xozJDI62OGRGc-fvCbPAtucG6cmSKL2VvM3vVKzQ=="
INFLUXDB_ORG = "cmp"
INFLUXDB_BUCKET = "BTC-USD-COINGECKO"
INFLUXDB_PREDICTIONS_BUCKET = "BTC-PREDICTIONS"

# Passo 1: Obter dados históricos do Bitcoin
def get_bitcoin_data():
    try:
        url = 'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart'
        params = {
            'vs_currency': 'usd',
            'days': '365',
            'interval': 'daily'
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        prices = data['prices']
        df = pd.DataFrame(prices, columns=['timestamp', 'price'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df
    except requests.exceptions.RequestException as e:
        print(f"Erro ao obter dados: {e}")
        return pd.DataFrame()

# Passo 2: Pré-processamento dos dados
def preprocess_data(df):
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(df['price'].values.reshape(-1, 1))
    return scaled_data, scaler

# Função para criar sequências de dados
def create_sequences(data, seq_length):
    X = []
    y = []
    for i in range(len(data) - seq_length):
        X.append(data[i:i+seq_length])
        y.append(data[i+seq_length])
    return np.array(X), np.array(y)

# Passo 3: Criar o modelo de rede neural
def create_model(seq_length):
    model = tf.keras.Sequential([
        tf.keras.layers.LSTM(50, return_sequences=True, input_shape=(seq_length, 1)),
        tf.keras.layers.LSTM(50, return_sequences=False),
        tf.keras.layers.Dense(25),
        tf.keras.layers.Dense(1)
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

# Passo 4: Treinar o modelo
def train_model(model, X_train, y_train, X_test, y_test, epochs=20, batch_size=32):
    history = model.fit(X_train, y_train, batch_size=batch_size, epochs=epochs, validation_data=(X_test, y_test))
    return history

# Passo 5: Fazer previsões e calcular a acurácia
def predict_and_evaluate(model, X_test, y_test, scaler):
    predictions = model.predict(X_test)
    predictions = scaler.inverse_transform(predictions)
    y_test = scaler.inverse_transform(y_test.reshape(-1, 1))
    
    # Calcular RMSE
    rmse = np.sqrt(np.mean((predictions - y_test) ** 2))
    
    # Calcular percentual de acurácia
    mae = np.mean(np.abs(predictions - y_test))
    mean_actual = np.mean(y_test)
    accuracy = 100 - (mae / mean_actual * 100)
    
    return predictions, rmse, accuracy

# Fazer previsões para o conjunto completo
def predict_full(model, data, scaler):
    predictions = model.predict(data)
    predictions = scaler.inverse_transform(predictions)
    return predictions

# Inserir dados no InfluxDB
def insert_to_influxdb(df, bucket):
    try:
        with InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG) as client:
            write_api = client.write_api(write_options=WriteOptions(batch_size=500, flush_interval=10_000))
            for _, row in df.iterrows():
                dt = row['timestamp']
                timestamp_ns = int(dt.timestamp() * 1e9)
                point = Point("bitcoin") \
                    .field("price", row['price']) \
                    .time(timestamp_ns, WritePrecision.NS)
                write_api.write(bucket=bucket, org=INFLUXDB_ORG, record=point)
            write_api.close()  # Ensure all data is written before closing the script
    except Exception as e:
        print(f"Erro ao inserir dados no InfluxDB: {e}")

# Inserir previsões no InfluxDB
def insert_predictions_to_influxdb(predictions, timestamps, bucket):
    try:
        with InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG) as client:
            write_api = client.write_api(write_options=WriteOptions(batch_size=500, flush_interval=10_000))
            for i, prediction in enumerate(predictions):
                dt = pd.Timestamp(timestamps[i])
                timestamp_ns = int(dt.timestamp() * 1e9)
                point = Point("bitcoin_predictions") \
                    .field("predicted_price", float(prediction)) \
                    .time(timestamp_ns, WritePrecision.NS)
                write_api.write(bucket=bucket, org=INFLUXDB_ORG, record=point)
            write_api.close()  # Ensure all data is written before closing the script
    except Exception as e:
        print(f"Erro ao inserir previsões no InfluxDB: {e}")

# Main function
def main():
    df = get_bitcoin_data()
    if df.empty:
        print("Falha ao obter dados do Bitcoin. Encerrando script.")
        return
    
    scaled_data, scaler = preprocess_data(df)
    seq_length = 100  # Usar 100 dias de dados para prever o próximo preço
    X, y = create_sequences(scaled_data, seq_length)

    if len(X) == 0 or len(y) == 0:
        print("Falha ao criar sequências de dados. Verifique o comprimento dos dados e seq_length.")
        return

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    if len(X_train) == 0 or len(X_test) == 0 or len(y_train) == 0 or len(y_test) == 0:
        print("Falha ao dividir os dados em conjuntos de treinamento e teste. Verifique os parâmetros de divisão.")
        return

    model = create_model(seq_length)
    train_model(model, X_train, y_train, X_test, y_test)
    
    # Prever preços futuros e calcular a acurácia
    predictions, rmse, accuracy = predict_and_evaluate(model, X_test, y_test, scaler)
    print(f"Acurácia do modelo (RMSE): {rmse}")
    print(f"Percentual de acurácia do modelo: {accuracy}%")

    # Prever preços futuros usando todo o conjunto de dados
    full_sequences = np.concatenate((X_train, X_test))
    full_timestamps = df['timestamp'][seq_length:].reset_index(drop=True)
    
    full_predictions = predict_full(model, full_sequences, scaler)
    
    # Inserir os dados históricos no InfluxDB
    insert_to_influxdb(df, INFLUXDB_BUCKET)
    
    # Criar DataFrame com timestamps para previsões
    prediction_df = pd.DataFrame({'timestamp': full_timestamps, 'predicted_price': full_predictions.flatten()})
    
    # Inserir previsões no InfluxDB
    insert_predictions_to_influxdb(prediction_df['predicted_price'].values, prediction_df['timestamp'].values, INFLUXDB_PREDICTIONS_BUCKET)
    
    print("Dados históricos e previsões inseridos no InfluxDB com sucesso!")

if __name__ == "__main__":
    main()