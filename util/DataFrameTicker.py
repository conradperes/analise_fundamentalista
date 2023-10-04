import yfinance as yf
import pandas as pd
from influxdb_client import Point

class DataFrameTicker:
    def __init__(self):
        self.start_period = None
        self.end_period = None

    def get_dataframe(self, ticker, start_period, end_period):
        print("Entrou no DataFrame")
        self.start_period = start_period
        self.end_period = end_period

        # Obter os dados do Yahoo Finance
        try:
            print("Antes do download no DataFrame")
            df = yf.download(ticker, start=self.start_period, end=self.end_period)
            print("Depois do download no DataFrame")
            return df
        except AttributeError as e:
            print(f"Erro ao obter dados do Yahoo Finance: {e}")
            return None  # Ou outra ação, dependendo do seu caso

    #prepare data to influxdb
    def prepare_data_to_influxdb(self, df, ticker):
    
        data_points = []
        for index, row in df.iterrows():
            data_point = Point(ticker) \
                .time(index) \
                .field("Open", row["Open"]) \
                .field("High", row["High"]) \
                .field("Low", row["Low"]) \
                .field("Close", row["Close"]) \
                .field("Adj Close", row["Adj Close"]) \
                .field("Volume", row["Volume"])
            
            data_points.append(data_point)
        return data_points
# Exemplo de uso:
# ticker_data = DataFrameTicker()
# df = ticker_data.get_dataframe("AAPL", "2022-01-01", "2023-01-01")
# if df is not None:
#     influx_measurement = "stock_data"
#     influx_tags = {"ticker": "AAPL"}
#     data_points = ticker_data.prepare_data_to_influxdb(df, influx_measurement, influx_tags)
#     print(data_points)
