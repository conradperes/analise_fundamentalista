docker stop influxdb
docker rm influxdb
docker run -d --name influxdb -p 8086:8086 -v influxdb_data:/var/lib/influxdb influxdb
docker run -d -p 27017:27017 --name mongodb-container my-mongodb