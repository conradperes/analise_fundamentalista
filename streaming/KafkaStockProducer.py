import yfinance as yf
from confluent_kafka import Producer, KafkaException
from datetime import date, datetime
import time
class KafkaStockProducer:
    def __init__(self, bootstrap_servers='localhost:9092'):
        self.bootstrap_servers = bootstrap_servers
        self.producer_conf = {'bootstrap.servers': self.bootstrap_servers}
        self.producer = None  # Inicializamos o produtor como None

    def initialize_producer(self):
        try:
            self.producer = Producer(self.producer_conf)
        except KafkaException as e:
            print(f"Erro ao inicializar o Kafka Producer: {e}")

    def get_dataframe(self, ticker, start_period, end_period):
        print("entrou no dataframe")
        start_period = start_period
        end_period = end_period
        #obter os dados do yahoo finance
        try:
            print("antes do download no dataframe")
            df = yf.download(ticker, start=start_period, end=end_period)
            print("depois do download no dataframe")
            return df
        except AttributeError as e:
            print(f"Erro ao obter dados do Yahoo Finance: {e}")
            return None  # Ou outra ação adequada, como retornar um DataFrame vazio ou levantar outra exceção

    def produce_to_kafka(self, stock_data, topic):
        if self.producer is None:
            print("O Kafka Producer não foi inicializado corretamente. Verifique as configurações.")
            return

        for index, row in stock_data.iterrows():
            # Obter a data e hora com microssegundos
            timestamp_with_micros = index.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            
            # Converter para bytes
            key_bytes = timestamp_with_micros.encode('utf-8')

            # Formatar a mensagem
            message = f"{timestamp_with_micros} {row['Close']} {row['Open']}"

            # Produzir a mensagem no tópico
            self.producer.produce(topic, key=key_bytes, value=message)

        # Aguardar até que todos os dados sejam enviados
        self.producer.flush()

# Exemplo de uso
if __name__ == "__main__":
    # Substitua 'AAPL' pelo símbolo da ação desejada e 'stock-quotes' pelo nome do tópico Kafka
    stock_symbol = 'BTC-USD'
    kafka_topic = 'stock-quotes'

    # Criar instância da classe KafkaStockProducer
    kafka_producer = KafkaStockProducer()

    # Inicializar o Kafka Producer
    kafka_producer.initialize_producer()

    # Verificar se o Kafka Producer foi inicializado corretamente
    if kafka_producer.producer is not None:
        # Obter dados da açãodata_atual = date.today()
        data_atual = date.today()
        primeiro_dia_do_ano = date(data_atual.year-3, 1, 1)
        stock_data = kafka_producer.get_dataframe(stock_symbol, primeiro_dia_do_ano, data_atual)

        # Produzir dados no tópico Kafka
        kafka_producer.produce_to_kafka(stock_data, kafka_topic)
