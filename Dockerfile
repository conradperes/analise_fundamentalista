# Use an official Python runtime as a parent image
FROM python:3.11
# Set the working directory to /app
WORKDIR /app
# Install any needed packages specified in requirements.txt
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --upgrade yfinance
#RUN pip uninstall numpy influxdb_client
#RUN pip install numpy influxdb_client
#RUN pip install --upgrade pip  pandas yfinance numpy mplfinance  plotly
# Copy the current directory contents into the container at /app
COPY . /app
# Run your script when the container launches
CMD ["python3", "analise_fundamentalista.py"]

