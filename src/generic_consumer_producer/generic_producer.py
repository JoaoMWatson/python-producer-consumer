from confluent_kafka import Producer
from confluent_kafka.error import KafkaError, ProduceError
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import MessageField, SerializationContext

from config import settings


class GenericKafkaProducer:
    def __init__(self, env, offset='earliest'):
        """Consumer class

        Args:
            topic (str): Destiny topic
            env (str): Environment how gonna be consumed
            offset (str): Offset config, earliest/latest
        """
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
