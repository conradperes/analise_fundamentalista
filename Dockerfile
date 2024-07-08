# Use a imagem oficial do Python
FROM python:3.11

WORKDIR /app
# Definir variáveis de ambiente
ENV INFLUXDB_DB cmp
ENV INFLUXDB_USER conrad
ENV INFLUXDB_USER_PASSWORD 711724Cope
ENV INFLUXDB_USER_READ conrad
ENV INFLUXDB_USER_WRITE conrad
ENV INFLUXDB_ORG cmp
ENV INFLUXDB_TOKEN export INFLUXDB_TOKEN=-x5Px0583Cj5u7TUlkDglb3NTcxWDYSdJpaOae0QIpDKOX7Kk3WusDQRxSfEWk7YS7s3om8GmnHbyblDe916FQ==
ENV ticker doge-usd

# Copiar o script Python para o contêiner
COPY analise_fundamentalista.py /app/analise_fundamentalista.py
COPY analise_fundamentalista_acoes.py /app/analise_fundamentalista_acoes.py
# Instalar bibliotecas Python necessárias
RUN pip install influxdb-client \
    plotly \
    yfinance \
    pandas \
    matplotlib \
    mplfinance

CMD ["python3", "-u", "analise_fundamentalista.py"]
