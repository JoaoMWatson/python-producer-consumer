from src.generic_consumer_producer.generic_consumer import GenericKafkaConsumer

test_1 = GenericKafkaConsumer('unit-updated', 'dev')

test_1.listener()