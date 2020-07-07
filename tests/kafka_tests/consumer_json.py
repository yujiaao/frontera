from json.decoder import JSONDecodeError

from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(group_id= 'group3', bootstrap_servers= ['localhost:9092'], value_deserializer=lambda m: json.loads(m.decode('ascii')))
consumer.subscribe(pattern= '^my.*')
try:
  for msg in consumer:
    print(msg)
except JSONDecodeError:
    print("json error")
