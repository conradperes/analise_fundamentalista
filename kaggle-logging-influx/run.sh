docker run -e INFLUXDB_URL=http://localhost:8086 \
           -e INFLUXDB_TOKEN=5h4SQ0LxxDq7hBLJrTsa9FT_bHDzeSItc1w5vOEoR6iF-ZBWwAONSbmeVgHiyWlGy7WmWaBj3cSutMLlCxsEpA== \
           -e INFLUXDB_ORG=cmp \
           -e INFLUXDB_BUCKET=application_logs \
           log_application
echo $INFLUXDB_TOKEN