from kafka import KafkaConsumer

consumer = KafkaConsumer('my_topic', group_id= 'group3',
                         bootstrap_servers= ['localhost:9092'],consumer_timeout_ms=10000)
for msg in consumer:
    print(msg)
