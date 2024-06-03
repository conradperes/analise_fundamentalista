# Esse projeto visa fazer uma analise fundamentalista baseado na pesquisa das cotações de qualquer ticker tanto da bolsa de valores, ou de qualquer blockchain via biblioteca do yahoo finance, e em seguida salvar essas cotações de diversos time franes, no modulo spark considerando um dataset dos últimos 10 anos.

Em seguida salvando as mesas no banco de dados 
time series Influxdb, deployado em um container
docker, trazendo assim flexibilidade de deploy para
qualquer pipeline que se deseja deployar, evitando assim 
o lockin.

além disso tem vários outros scripts de machine learning,
utilizando varias abordagens de diderentes algoritmos.

Na ultima parte um teste que utiliza Jupyter notebooks 
para fazer os inserts no Influxdb, de maneira ultra eficiente,
usando a biblioteca pyspark baseada no framework
de big data ultra conhecido apache spark.
