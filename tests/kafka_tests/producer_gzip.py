from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers=['localhost:9092'], compression_type='gzip')
future = producer.send('my_topic' ,  key= b'key_3', value= b'value_3', partition= 0)
future.get(timeout= 10)

'''
发送msgpack消息
msgpack为MessagePack的简称，是高效二进制序列化类库，比json高效

producer = KafkaProducer(value_serializer=msgpack.dumps)
producer.send('msgpack-topic', {'key': 'value'})
'''
