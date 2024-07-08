# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt requirements.txt

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set environment variables for InfluxDB
ENV INFLUXDB_URL=http://localhost:8086
ENV INFLUXDB_TOKEN=b_npgI2_h0FvQmol1lYFN1vCvxAuIZYtaPW9k_1TK4CSHduwhNwIk8gMEYh4XqKZEXWXVyT2MAmtEsRyUtTOTw==
ENV INFLUXDB_ORG=cmp
ENV INFLUXDB_BUCKET=application_logs

# Copy kaggle.json to the container
COPY kaggle.json /root/.kaggle/kaggle.json

# Set permissions for kaggle.json
RUN chmod 600 /root/.kaggle/kaggle.json

# Run the application
CMD ["python", "kaggle-logging.py"]