from argparse import ArgumentParser

from salesdatagen import generator
from salesdatagen.common import make_producer
from salesdatagen.customer import CustomerRepo, CUSTOMER_AVRO_SCHEMA
from salesdatagen.order import OrderRepo, ORDER_AVRO_SCHEMA
from salesdatagen.product import ProductRepo, PRODUCT_AVRO_SCHEMA


if __name__ == '__main__':
    parser = ArgumentParser()
    # parser.add_argument('action', choices=['generate'])
    parser.add_argument('--interval', type=int, help='seconds between data generation', default=30)
    parser.add_argument('--intervals', type=int, help='number of intervals', default=-1)

    args = parser.parse_args()

    producer_args = ('http://localhost:8081', 'localhost:9092')

    customer_producer = make_producer(CUSTOMER_AVRO_SCHEMA, *producer_args)
    product_producer = make_producer(PRODUCT_AVRO_SCHEMA, *producer_args)
    order_producer = make_producer(ORDER_AVRO_SCHEMA, *producer_args)

    customer_repo = CustomerRepo(None, 'customers', customer_producer, 'customers')
    product_repo = ProductRepo(None, 'products', product_producer, 'products')
    order_repo = OrderRepo(None, 'orders', order_producer, 'orders')

    generator.seed_customers(customer_repo)
    generator.seed_products(product_repo)

    generator.generate_orders(
        order_repo,
        customers=customer_repo.items,
        products=product_repo.items,
        interval=args.interval,
        intervals=args.intervals
    )
