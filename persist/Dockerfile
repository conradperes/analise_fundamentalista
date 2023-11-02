FROM ubuntu:20.04
# Copy the Python script into the container
COPY save-crypto.py /save-crypto.py
COPY variables.env /variables.env
# Install Python and required packages
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install influxdb matplotlib influxdb_client plotly yfinance mplfinance
#RUN echo $INFLUXDB_TOKEN > /token.txt
# Command to run on container start

CMD ["sh", "-c", "python3 save-crypto.py"]