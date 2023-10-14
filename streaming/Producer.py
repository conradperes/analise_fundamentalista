import yfinance as yf
from confluent_kafka import Producer

class Producer:
    def __init__(self, bootstrap_servers='localhost:9092'):
        self.bootstrap_servers = bootstrap_servers
        self.producer_conf = {'bootstrap.servers': self.bootstrap_servers}
        self.producer = Producer(self.producer_conf)

    def fetch_stock_data(self, symbol, start_date="2021-01-01", end_date="2023-01-01"):
        stock_data = yf.download(symbol, start=start_date, end=end_date)
        print(stock_data.head(7))
        return stock_data

    def produce_to_kafka(self, stock_data, topic):
        for index, row in stock_data.iterrows():
            message = f"{index.strftime('%Y-%m-%d')} {row['Close']}"
            self.producer.produce(topic, value=message)

        # Aguardar até que todos os dados sejam enviados
        self.producer.flush()

# Exemplo de uso
if __name__ == "__main__":
    # Substitua 'AAPL' pelo símbolo da ação desejada e 'stock-quotes' pelo nome do tópico Kafka
    stock_symbol = 'BTC-USD'
    kafka_topic = 'stock-quotes'

    # Criar instância da classe KafkaStockProducer
    kafka_producer = Producer()

    # Obter dados da ação
    stock_data = kafka_producer.fetch_stock_data(stock_symbol)

    # Produzir dados no tópico Kafka
    kafka_producer.produce_to_kafka(stock_data, kafka_topic)
