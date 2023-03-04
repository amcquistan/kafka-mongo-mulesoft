# Integration Pattern: Kafka, Kafka Connect, MongoDB & MuleSoft

Docker based example integration pattern utilizing MongoDB, Apache Kafka, and MuleSoft. 
A Python based program generates fictitious sales data representing customer, product, and order domains. The customer and product domain data are persisted directly to MongoDB within the Python program where as the orders are published into Kafka brokers. Therefor, Apache Kafka is the data ingestion target, Kafka Connect is then used as a configuration driven approach to pipeline data from Kafka into MongoDB, and finally the MuleSoft rapid API development platform is utilized for serving data from MongoDB via a REST interface. 


## Running Locally

1) Start Docker Compose Services

```
docker-compose up --build
```

2) Start salesdatagen Python program to start generating sales order data

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m salesdatagen
```

3) Verify Sales Orders Data Being Published

```
docker exec -it schema-registry kafka-avro-console-consumer --from-beginning \
  --bootstrap-server broker:29092 --topic orders \
  --property "schema.registry.url=http://localhost:8081"
```

4) Start the MongoDB Kafka Connect Sink Connector

```
http PUT :8083/connectors/orders-sink/config @orders-sink.json
```

5) View Orders Data in MongoDB

```
docker exec -it mongosh mongosh mongodb://developer:Develop3r@mongodb:27017
use sales
db.orders.find({})
```
