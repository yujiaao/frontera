from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
future = producer.send('my_topic' , key= b'my_key', value= b'my_value', partition= 0)
result = future.get(timeout= 10)
print(result)
