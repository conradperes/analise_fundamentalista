# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app
# Install Python
RUN apt-get update && apt-get install -y python3

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Use an official InfluxDB image as a parent image
FROM influxdb

# Expose the default InfluxDB HTTP API port
EXPOSE 8086

# Run InfluxDB in the background
CMD ["influxd"]
# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run your script when the container launches
CMD ["python3", "./analise_fundamentalista.py"]
