# Use an official InfluxDB runtime as a parent image
FROM influxdb:latest

# Set the environment variables for InfluxDB
ENV INFLUXDB_DB=mydb
ENV INFLUXDB_ADMIN_USER=conrad
ENV INFLUXDB_ADMIN_PASSWORD=711724Cope
ENV INFLUXDB_USER=conrad
ENV INFLUXDB_USER_PASSWORD=711724Cope

# Set the environment variable for InfluxDB Python script
#ENV INFLUXDB_TOKEN="Cf15LHUY4Fc9QwfD61zremmmVHhOgzsZtgKwgxIPbPi48hz1gUDkUTg-5ZMpSMF_9yrMdCrv3fMebB_Ow3gb4g=="

# Expose the InfluxDB port
EXPOSE 8086

# Copy the Python script into the container
COPY save-crypto.py /save-crypto.py

# Install Python and required packages
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install influxdb matplotlib influxdb_client plotly yfinance mplfinance
#RUN echo $INFLUXDB_TOKEN > /token.txt
# Command to run on container start
CMD ["sh", "-c", "influxd"]
CMD ["sh", "-c", "python3 save-crypto.py"]