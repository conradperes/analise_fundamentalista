# Use an official Python runtime as a parent image
FROM python:3.11.0a4

# Set the working directory to /app
WORKDIR /app

# Install any needed packages specified in requirements.txt
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

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
CMD ["python", "analise_fundamentalista.py"]
