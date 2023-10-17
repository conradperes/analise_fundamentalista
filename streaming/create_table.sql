create TABLE btc_usd_table
 (key string primary key,
  value string)
 with
 (kafka_topic='BTC-USD',
  value_format='json',
   key_format='json');