from src.generic_consumer_producer.generic_consumer import GenericKafkaConsumer

test_1 = GenericKafkaConsumer('dev')

test_1.listener('unit-updated')
