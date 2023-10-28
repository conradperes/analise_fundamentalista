import os
import yfinance as yf
from confluent_kafka import Producer, KafkaException
from datetime import date, datetime
from influxdb_client import InfluxDBClient, Point
import json

class KafkaStockProducer:
    def __init__(self, bootstrap_servers='localhost:9092'):
        self.bootstrap_servers = bootstrap_servers
        self.producer_conf = {'bootstrap.servers': self.bootstrap_servers}

    def __enter__(self):
        self.producer = Producer(self.producer_conf)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.producer is not None:
            self.producer.flush()
            self.producer = None

    def prepare_data_for_kafka(self, df, ticker):
        data_for_kafka = []
        for index, row in df.iterrows():
            data_point = {
                "ticker": ticker,
                "time": index.strftime('%Y-%m-%d'),  # Converte o Timestamp para uma string formatada
                "Open": row["Open"],
                "High": row["High"],
                "Low": row["Low"],
                "Close": row["Close"],
                "Adj Close": row["Adj Close"],
                "Volume": row["Volume"]
            }
            data_for_kafka.append(data_point)
        return data_for_kafka

    def get_dataframe(self, ticker, start_period, end_period):
        try:
            df = yf.download(ticker, start=start_period, end=end_period)
            return df
        except Exception as e:
            print(f"Erro ao obter dados do Yahoo Finance: {e}")
            return None

    def produce_to_kafka(self, data_points, topic):
        for data_point in data_points:
            key = data_point['ticker']
            value = json.dumps(data_point)
            self.producer.produce(topic, key=key, value=value)
            print(f"produziu o seguinte valor:{value}")

if __name__ == "__main__":
    stock_symbol = os.environ.get("ticker")
    kafka_topic = stock_symbol  # Substitua com o nome do tópico Kafka desejado
    
    with KafkaStockProducer() as kafka_producer:
        data_atual = date.today()
        primeiro_dia_do_ano = date(data_atual.year - 20, 1, 1)
        stock_data = kafka_producer.get_dataframe(stock_symbol, primeiro_dia_do_ano, data_atual)
        
        if stock_data is not None:
            data_points = kafka_producer.prepare_data_for_kafka(stock_data, stock_symbol)
            kafka_producer.produce_to_kafka(data_points, kafka_topic)
