# Construir a imagem
docker build -t influxdb .

# Executar o contêiner
docker run -p 8086:8086 --name influxdb-container influxdb
