from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers=['localhost:9092'], compression_type='gzip')
future = producer.send('my_topic' ,  key= b'key_3', value= b'value_3', partition= 0)
future.get(timeout= 10)
