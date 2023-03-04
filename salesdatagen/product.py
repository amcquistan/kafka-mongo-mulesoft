
from salesdatagen.common import BaseRepo

from pydantic import BaseModel


class Product(BaseModel):
    id: str
    name: str
    price: int
    created: int
 

PRODUCT_AVRO_SCHEMA = '''
{
  "name": "Product",
  "type": "record",
  "fields": [
    {
      "name": "id",
      "type": "string"
    },
    {
      "name": "name",
      "type": "string"
    },
    {
      "name": "price",
      "type": "int"
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


class ProductRepo(BaseRepo):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

