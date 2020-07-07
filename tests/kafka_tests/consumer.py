from kafka import KafkaConsumer

consumer = KafkaConsumer('my_topic', group_id= 'group3',
                         bootstrap_servers= ['localhost:9092'])
for msg in consumer:
    print(msg)
