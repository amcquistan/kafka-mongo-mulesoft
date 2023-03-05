import os

from argparse import ArgumentParser

from dotenv import load_dotenv

from salesdatagen import generator
from salesdatagen.common import make_db_client, make_producer
from salesdatagen.customer import CustomerRepo, CUSTOMER_AVRO_SCHEMA
from salesdatagen.order import OrderRepo, ORDER_AVRO_SCHEMA
from salesdatagen.product import ProductRepo, PRODUCT_AVRO_SCHEMA


load_dotenv(dotenv_path=os.getenv('ENV_FILE' , 'local.env'), verbose=True)


if __name__ == '__main__':
    parser = ArgumentParser()
    # parser.add_argument('action', choices=['generate'])
    parser.add_argument('--interval', type=int, help='seconds between data generation', default=30)
    parser.add_argument('--intervals', type=int, help='number of intervals', default=-1)

    args = parser.parse_args()

    producer_args = (os.environ['SCHEMA_REGISTRY'], os.environ['BOOTSTRAP_BROKERS'])

    db_clinet = make_db_client(os.environ['DB_PROTOCOL'], os.environ['DB_USER'], os.environ['DB_PASSWORD'], os.environ['DB_HOST'])

    customer_producer = make_producer(CUSTOMER_AVRO_SCHEMA, *producer_args)
    product_producer = make_producer(PRODUCT_AVRO_SCHEMA, *producer_args)
    order_producer = make_producer(ORDER_AVRO_SCHEMA, *producer_args)

    customer_repo = CustomerRepo(db_clinet, os.environ['DB_NAME'], 'customers', customer_producer, 'customers')
    product_repo = ProductRepo(db_clinet, os.environ['DB_NAME'], 'products', product_producer, 'products')
    order_repo = OrderRepo(db_clinet, os.environ['DB_NAME'], 'orders', order_producer, 'orders')

    generator.seed_customers(customer_repo)
    generator.seed_products(product_repo)

    generator.generate_orders(
        order_repo,
        customers=customer_repo.items,
        products=product_repo.items,
        interval=args.interval,
        intervals=args.intervals
    )
