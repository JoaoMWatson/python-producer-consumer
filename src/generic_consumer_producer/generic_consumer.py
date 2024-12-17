from confluent_kafka import Consumer
from confluent_kafka.error import ConsumeError, KafkaError
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.serialization import MessageField, SerializationContext

from config import settings

class GenericKafkaConsumer:
    def __init__(
        self,
        topic,
        env,
        offset='earliest'
    ):
        """Consumer class

        Args:
            topic (str): Destiny topic
            env (str): Environment how gonna be consumed
            offset (str): Offset config, earliest/latest
        """
        self.topic = topic
        self.env = env
        self.offset = offset
        self._secrets = ''

        if env == 'dev' or 'develop':
            self._secrets = settings.dev
        if env == 'hml' or 'homol':
            self._secrets = settings.hml

    def _create_config(self, type):
        if type == 'consumer':
            config = {
                'bootstrap.servers': self._secrets.CC_BOOTSTRAP_SERVER,
                'group.id': self._secrets.CONSUMER_GROUP,
                'auto.offset.reset': self.offset,
                'enable.auto.commit': 'false',
                'security.protocol': 'SASL_SSL',
                'sasl.mechanisms': 'PLAIN',
                'sasl.username': self._secrets.CC_API_KEY,
                'sasl.password': self._secrets.CC_API_SECRET,
            }
        if type == 'schema':
            config = {
                'url': self._secrets.SR_URL,
                'basic.auth.user.info': '{}:{}'.format(
                    self._secrets.SR_KEY, self._secrets.SR_SECRET
                ),
            }

        return config

    def message_handler(self, message_raw):
        sr_config = self._create_config('schema')

        schema_registry_client = SchemaRegistryClient(sr_config)
        avro_deserializer = AvroDeserializer(schema_registry_client)

        message_decoded = avro_deserializer(
            message_raw.value(),
            SerializationContext(message_raw.topic(), MessageField.VALUE),
        )

        return message_decoded

    def listener(self):
        consumer_config = self._create_config('consumer')

        consumer = Consumer(consumer_config)
        consumer.subscribe([self.topic])

        try:
            running = True
            while running:
                msg = consumer.poll()
                if not msg.error():
                    message = self.message_handler(msg)
                    print(message)
                elif msg.error().code() != KafkaError._PARTITION_EOF:
                    print(msg.error())
                    running = False

        except KeyboardInterrupt as e:
            print('\nCONSUMER - Ending program')

        except ConsumeError as e:
            print(f'\nCONSUMER - Error while consume: {e}')
        
        except ValueError as e:
            print(f'\nCONSUMER - Error while decode: {e.with_traceback}')

        finally:
            print('Closing consumer')
            consumer.close()

