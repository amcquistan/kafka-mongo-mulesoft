
from pydantic import BaseModel

from salesdatagen.common import BaseRepo


class Customer(BaseModel):
    id: str
    first_name: str
    last_name: str
    created: int


CUSTOMER_AVRO_SCHEMA = '''
{
  "name": "Customer",
  "type": "record",
  "fields": [
    {
      "name": "id",
      "type": "string"
    },
    {
      "name": "first_name",
      "type": "string"
    },
    {
      "name": "last_name",
      "type": "string"
    },
    {
      "name": "created",
      "type": {
          "type": "long",
          "logicalType": "timestamp-millis"
      }
    }
  ]
}
'''


class CustomerRepo(BaseRepo):
    def __init__(self, db_client, db_name, db_collection, producer, topic, *args, **kwargs):
        super().__init__(db_client, db_name, db_collection, producer, topic, *args, **kwargs)

    # def save(self, model: BaseModel, cache=True) -> BaseModel:
    #     self.db_client.custermers.insert_one(model.dict())
    #     return super().save(model, cache=cache)

        
