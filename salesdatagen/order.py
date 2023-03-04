
from typing import List

from pydantic import BaseModel

from salesdatagen.common import BaseRepo
from salesdatagen.customer import Customer
from salesdatagen.product import Product


class LineItem(BaseModel):
    product: Product
    quantity = 1


class Order(BaseModel):
    id: str
    status: str
    created: int
    customer: Customer
    items: List[LineItem]


ORDER_AVRO_SCHEMA = '''
{
  "name": "Order",
  "type": "record",
  "fields": [
    {
      "name": "id",
      "type": "string"
    },
    {
      "name": "status",
      "type": "string"
    },
    {
      "name": "created",
      "type": {
          "type": "long",
          "logicalType": "timestamp-millis"
      }
    },
    {
      "name": "customer",
      "type": {
        "type": "record",
        "name": "Customer",
        "fields": [{
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
        }]
      }
    },
    {
      "name": "items",
      "type": {
        "type": "array",
        "items": {
          "name": "LineItem",
          "type": "record",
          "fields": [
            {
              "name": "product",
              "type": {
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
            },
            {
              "name": "quantity",
              "type": "int"
            }
          ]
        }
      }
    }
  ]
}
'''


class OrderRepo(BaseRepo):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
