import logging
from abc import ABC
from typing import List

from confluent_kafka import SerializingProducer
from confluent_kafka.admin import AdminClient, NewTopic

from confluent_kafka.serialization import StringSerializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer

from pydantic import BaseModel


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class BaseRepo(ABC):
    def __init__(self, db_client, db_name, producer, topic, *args, **kwargs):
        self.db_client = db_client
        self.producer = producer
        self.db_name = db_name
        self.topic = topic
        self.items = []

    def save(self, model: BaseModel) -> BaseModel:
        self.items.append(model)

    def fetch(self, id: str) -> BaseModel:
        results = filter(lambda x: x.id == id, self.items)
        return results[0]

    def fetch_all(self) -> List[BaseModel]:
        return self.items

    def publish(self, model: BaseModel):
        self.producer.produce(
           topic=self.topic,
           key=model.id,
           value=model,
           on_delivery=ProducerCallback(model)
        )

    def flush(self):
       if self.db_client:
          pass
       if self.producer:
          self.producer.flush()


def make_producer(schema, schema_reg_url, bootstrap_urls) -> SerializingProducer:
  schema_reg_client = SchemaRegistryClient({'url': schema_reg_url})
  avro_serializer = AvroSerializer(schema_reg_client,
                                  schema,
                                  lambda model, ctx: model.dict())
  return SerializingProducer({'bootstrap.servers': bootstrap_urls,
                            'linger.ms': 300,
                            'enable.idempotence': 'true',
                            'max.in.flight.requests.per.connection': 1,
                            'acks': 'all',
                            'key.serializer': StringSerializer('utf_8'),
                            'value.serializer': avro_serializer,
                            'partitioner': 'murmur2_random'})


class ProducerCallback:
  def __init__(self, model):
    self.model = model

  def __call__(self, err, msg):
      if err:
        logger.error(f"Failed to produce {self.model}", exc_info=err)
      else:
        logger.info(f"""
          Successfully produced {self.model}
          partition {msg.partition()}
          at offset {msg.offset()}""")

