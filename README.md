# Fundamental Analysis Project

This project performs fundamental analysis based on stock quotes or blockchain data using the Yahoo Finance library. It saves these quotes from various time frames in a Spark module, covering the past 10 years, and then stores them in a time series database, InfluxDB, deployed in a Docker container. This setup provides flexible deployment options for any pipeline, avoiding vendor lock-in.

Additionally, the repository contains several machine learning scripts using different algorithms. The final part includes a Jupyter notebook test for efficient data insertion into InfluxDB using PySpark with the well-known big data framework, Apache Spark.

## Features

- **Stock and Blockchain Data Analysis**: Fetches and processes data from Yahoo Finance.
- **Spark Integration**: Utilizes Apache Spark for data processing.
- **Time Series Database**: Stores processed data in InfluxDB for efficient time-series data handling.
- **Docker Deployment**: Ensures flexible and portable deployment.
- **Machine Learning Scripts**: Includes various ML algorithms for data analysis.
- **Jupyter Notebooks**: Provides examples and tests for efficient data handling.
- **Kafka Streaming**: Uses Kafka for real-time data streaming with producer and consumer setup.
- **Kafka Connect**: Integrates with Kafka Connect for streaming data to Huawei Cloud OBS, similar to AWS S3.

## Getting Started

### Prerequisites

- Docker
- Apache Spark
- InfluxDB
- Kafka
- Python libraries: `yfinance`, `pyspark`, `influxdb-client`

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/conradperes/analise_fundamentalista.git
   cd analise_fundamentalista

2.	Set up Docker containers for InfluxDB and Kafka (Streaming folder):
	```sh
	cd analise_fundamentalista/streaming
	./setup.sh
	docker-compose up -d

3.	Install required Python libraries:
	```sh
	pip install yfinance pyspark influxdb-client


### Usage

1.	Data Fetching and Processing:
•	Use the provided scripts to fetch and process data from Yahoo Finance.
2.	Machine Learning:
•	Run the machine learning scripts located in the ml_scripts directory.
3.	Jupyter Notebooks:
•	Explore the notebooks in the notebooks directory for efficient data insertion into InfluxDB using PySpark.
4.	Kafka Streaming:
•	Navigate to the streaming folder to set up Kafka producer and consumer.
•	Start Kafka Connect to stream data to Huawei Cloud OBS.

Kafka Streaming Setup

1.	Producer:
•	The producer script generates data and sends it to the Kafka topic.
2.	Consumer:
•	The consumer script reads data from the Kafka topic and processes it.
3.	Kafka Connect:
•	Configure Kafka Connect with connectors to stream data from the Kafka topic to Huawei Cloud OBS.

### Shell Scripts

•Building and Creating Containers: Each folder contains shell scripts to help build and create the containers. 
Run the following commands to use these scripts:

•InfluxDB Setup:

```cd analise_fundamentalista/influxdb
   ./setup_influxdb.sh
```
•	Kafka Setup:

```cd analise_fundamentalista/streaming
   ./setup_kafka.sh
```
•	Spark Setup:

```cd analise_fundamentalista/spark
./setup_spark.sh
```


•Contributing

Contributions are welcome! Please fork this repository and submit pull requests.

License

This project is licensed under the MIT License.


