import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import pandas as pd
from datetime import datetime
import re
class QueryInflux:
    
    
    def getToken():
        token = os.environ.get("INFLUXDB_TOKEN")
        return token
    

    def retornar_data(data):
        #input_string = "0 01/01/2023"
        # Usar expressão regular para encontrar a data no formato DD/MM/YYYY
        match = re.search(r'\d{2}/\d{2}/\d{4}', data)

        if match:
            date_string = match.group()  # Extrair a data correspondente
            print(date_string)
        else:
            print("Data não encontrada na string.")
        return date_string
    
    
    def get_dataframeByBucketInflux(bucket):
        token = os.environ.get("INFLUXDB_TOKEN")
        org = "cmp"
        url = "http://localhost:8086"
        #print(token)
        client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
        query_api = client.query_api()

        query = f"""from(bucket: "{bucket}")
        |> range(start: -1y, stop: now())
        |> filter(fn: (r) => r["_measurement"] == "{bucket}")
        |> filter(fn: (r) => r["_field"] == "Close")
        |> keep(columns: ["_time", "_value"])
        """

        #|> filter(fn: (r) => r._measurement == "measurement")
        tables = query_api.query(query, org="cmp")
        # Inicializar listas vazias para as colunas
        
        close_values = []
        date_values = []
        # Extrair os valores da consulta e adicioná-los às listas
        for table in tables:
            for record in table.records:
                time_value = record.values["_time"].strftime('%d/%m/%Y')
                match = re.search(r'\d{2}/\d{2}/\d{4}', time_value)
                if match:
                    date_string = match.group()  # Extrair a data correspondente
                    #print(date_string)
                    date_values.append(date_string)
                else:
                    print("Data não encontrada na string.")
                
                close_values.append(record.values["_value"])

        # Criar um DataFrame Pandas com as colunas "_time" e "_value"
        df = pd.DataFrame({"index": date_values, "Close": close_values})
        return df
    
    df = get_dataframeByBucketInflux("MATIC-USD")
    print(df.head(2))#['Close']

    