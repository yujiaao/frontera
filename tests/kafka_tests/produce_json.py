from kafka import KafkaProducer
import json

producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=lambda m: json.dumps(m).encode('ascii'))
future = producer.send('my_topic' ,  value= {'value_1' : 'value_2'}, partition= 0)
future.get(timeout= 10)
