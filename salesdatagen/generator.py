
import random
import uuid

from datetime import datetime
from time import sleep
from typing import List

from faker import Faker

from salesdatagen import aggregation
from salesdatagen.customer import Customer
from salesdatagen.common import BaseRepo
from salesdatagen.product import Product
from salesdatagen.order import Order, LineItem



def created_timestamp() -> int:
    """current timestamp in milliseconds since epoch"""
    return int(datetime.now().timestamp() * 1000)


def make_uuid() -> str:
    """uuid as a string"""
    return str(uuid.uuid4())


def seed_products(repo: BaseRepo) -> List[Product]:
    """populate a default collection of products for random sales generation"""
    return [
        repo.save(Product(id=make_uuid(), name="Wacky Widget", price=10, created=created_timestamp())),
        repo.save(Product(id=make_uuid(), name="Amazing Chia Pet", price=8, created=created_timestamp())),
        repo.save(Product(id=make_uuid(), name="Super Slinky", price=5, created=created_timestamp())),
        repo.save(Product(id=make_uuid(), name="Silly String", price=12, created=created_timestamp())),
        repo.save(Product(id=make_uuid(), name="Stress Ball", price=10, created=created_timestamp())),
    ]


def seed_customers(repo: BaseRepo, num = 20) -> List[Customer]:
    """populate a variable collection of random customers for sales generation """
    faker = Faker()
    customers = []
    for _ in range(num):
        customers.append(repo.save(Customer(
            id=make_uuid(),
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            created=created_timestamp()
        )))
    return customers


def generate_orders(
        repo: BaseRepo,
        interval = 30,
        intervals = -1,
        customers: List[Customer] = None,
        products: List[Product] = None,
        save = False
):
    """generate random sales orders with given customers and products"""
    i = 0

    while intervals == -1 or i <= intervals:
        customer = random.choice(customers)
        n_items = random.randint(1, len(products))
        line_items = []
        random.shuffle(products)
        for j in range(n_items):
            line_items.append(LineItem(
                product=products[j],
                quantity = random.randint(1, 20)
            ))

        order = Order(
            customer=customer,
            id=make_uuid(),
            status='CREATED',
            items=line_items,
            created=created_timestamp()
        )
        if save:
            repo.save(order)
        else:
            repo.publish(order)

        repo.flush()

        aggregation.customer_revenue(repo.db_client, "sales", "orders", "customer_revenue")
        aggregation.product_revenue(repo.db_client, "sales", "orders", "product_revenue")

        sleep(interval)
        i += 1

