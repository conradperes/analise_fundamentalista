# Use an official Jupyter PySpark Notebook image as a parent image
FROM jupyter/pyspark-notebook:latest

# Install additional dependencies
USER root
RUN pip install influxdb yfinance

# Set the working directory to /app
WORKDIR /app

# Copy the local code to the container
COPY . /app

CMD ["python3", "SaveWithSpark.py"]
