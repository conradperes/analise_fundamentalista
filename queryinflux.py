

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import plotly.graph_objs as go
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime, timedelta
import requests

class QueryInflux:
    #connect to influxdb
    def get_influx_client():
        token = os.environ.get("INFLUXDB_TOKEN")
        org = "cmp"
        url = "http://localhost:8086"
        print(token)
        client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
        print('depois de conectar')
        return client

    def persist_influxdb(client, bucket, measurement, data_points):
        print('antes de escrever')
        write_api = client.write_api(write_options=SYNCHRONOUS)
        write_api.write(bucket=bucket, org="cmp", record=data_points)
        print('depois de escrever')

    #create api call of coindesk to retrieve btc price of 2 years
    def get_btc_usd_prices():
        start_date = (datetime.now() - timedelta(days=365 * 4)).date()  # Últimos 2 anos
        print(start_date)
        end_date = datetime.now().date()
        print(end_date)
        api_url = f"https://api.coindesk.com/v1/bpi/historical/close.json?start={start_date}&end={end_date}"
        print(api_url)
        response = requests.get(api_url)
        data = response.json()
        return data

    #prepare data to influxdb
    def prepare_data_to_influxdb(data):
        data_points = []
        for date, price in data["bpi"].items():
            timestamp = datetime.strptime(date, "%Y-%m-%d")
            data_points.append(Point("btc_usd_prices").time(timestamp).field("price_usd", float(price)))
        return data_points
    
    #prepare data to plot
    def prepare_data_to_plot(data):
        dates = [datetime.strptime(date, "%Y-%m-%d") for date in data["bpi"].keys()]
        prices = [float(price) for price in data["bpi"].values()]
        return dates, prices
    #plot data
    def plot_data(dates, prices):
        trace = go.Scatter(x=dates, y=prices, mode="lines", name="BTC-USD Prices")
        layout = go.Layout(
            title="Cotações de BTC-USD do Mês Atual (2023)",
            xaxis_title="Data",
            yaxis_title="Preço (USD)",
        )
        fig = go.Figure(data=[trace], layout=layout)
        fig.show()

    def main():
        client = get_influx_client()
        bucket="bitcoinmf"
        measurement = 'btc_usd_prices'
        data = get_btc_usd_prices()
        data_points = prepare_data_to_influxdb(data)
        persist_influxdb(client, bucket, measurement, data_points)
        dates, prices = prepare_data_to_plot(data)
        plot_data(dates, prices)