import logging
import pandas as pd
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import os
import time

import kaggle.api # type: ignore

class SingletonMeta(type):
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class InfluxDBConnection(metaclass=SingletonMeta):
    def __init__(self):
        self.host = os.getenv("INFLUXDB_URL", "http://localhost:8086")
        self.token = os.getenv("INFLUXDB_TOKEN",  "b_npgI2_h0FvQmol1lYFN1vCvxAuIZYtaPW9k_1TK4CSHduwhNwIk8gMEYh4XqKZEXWXVyT2MAmtEsRyUtTOTw==")
        self.org = os.getenv("INFLUXDB_ORG", "cmp")
        self.client = self.create_client()


    def create_client(self):
        if not self.token:
            raise ValueError("INFLUXDB_TOKEN is not set in the environment variables.")

        max_retries = 10
        retry_delay = 10
        for attempt in range(max_retries):
            try:
                client = InfluxDBClient(url=self.host, token=self.token, org=self.org, timeout=30_000, retries=5)
                print("Conexão com InfluxDB realizada com sucesso!")
                return client
            except Exception as e:
                print(f"Tentativa {attempt + 1} falhou: {e}")
                if attempt + 1 == max_retries:
                    raise
                time.sleep(retry_delay)

class KaggleLogging:
    def __init__(self, dataset_name):
        self.dataset_name = dataset_name
        self.client = InfluxDBConnection().client
        self.bucket = os.getenv("INFLUXDB_BUCKET", "application_logs")
        self.org = os.getenv("INFLUXDB_ORG", "cmp")

    def setup_logging(self):
        # Create InfluxDB log handler
        influxdb_handler = InfluxDBHandler(self.client, self.bucket, self.org)
        influxdb_handler.setLevel(logging.INFO)

        # Create logger
        logger = logging.getLogger('influxdb_logger')
        logger.setLevel(logging.INFO)

        # Add handlers
        logger.addHandler(influxdb_handler)
        
        return logger

    def download_kaggle_dataset(self):
        kaggle.api.authenticate()
        kaggle.api.dataset_download_files(self.dataset_name, path='.', unzip=True)
        extracted_file = 'train_and_test2.csv'
        if os.path.exists(extracted_file):
            return extracted_file
        else:
            raise FileNotFoundError(f"{extracted_file} not found after download.")

    def log_titanic_data(self, logger, df):
        for index, row in df.iterrows():
            logger.info(f"Passenger: {row.get('Passengerid', 'N/A')}, Survived: {row.get('2urvived', 'N/A')}, Age: {row.get('Age', 'N/A')}, Fare: {row.get('Fare', 'N/A')}")

    def run(self):
        logger = self.setup_logging()

        # Download dataset
        csv_file = self.download_kaggle_dataset()

        # Read dataset
        df = pd.read_csv(csv_file)

        # Print column names to debug
        print("Column names:", df.columns)

        # Log some example data from the dataset
        self.log_titanic_data(logger, df.head(10))

class InfluxDBHandler(logging.Handler):
    def __init__(self, client, bucket, org):
        logging.Handler.__init__(self)
        self.client = client
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.bucket = bucket
        self.org = org

    def emit(self, record):
        log_entry = self.format(record)
        point = Point("application_logs") \
            .tag("level", record.levelname) \
            .field("message", log_entry)
        try:
            self.write_api.write(bucket=self.bucket, org=self.org, record=point)
        except Exception as e:
            print(f"Erro ao escrever no InfluxDB: {e}")

if __name__ == "__main__":
    dataset_name = 'heptapod/titanic'
    kaggle_logging = KaggleLogging(dataset_name)
    try:
        kaggle_logging.run()
    except Exception as e:
        print(f"Erro: {e}")
