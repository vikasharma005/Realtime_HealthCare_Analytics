import os
import time
import pandas as pd
import json
import asyncio
from asyncio import log
from decimal import Decimal
from aiokafka.consumer import AIOKafkaConsumer

from cassandra import ConsistencyLevel
from cassandra.query import SimpleStatement,BatchStatement
from aiocassandra import aiosession
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider


#Configuration
topic =  'patient_data'
#kafka_broker_url = os.environ.get('KAFKA_BROKER_URL')
kafka_broker_url = 'localhost:9092'

cluster = Cluster(
    contact_points=['localhost'],
    auth_provider=PlainTextAuthProvider(username='cassandra', password='cassandra')
)
session = cluster.connect()
session.default_fetch_size = 50000
session.set_keyspace('healthcare_db')

def batch_to_cassandra(payload):
    cql = """INSERT INTO healthcare_db.device_patient(
                id,name,age,gender,phone,address,
                condition,bmi,status,device_id,reading_id,heart_rate,
                blood_pressure_top,blood_pressure_bottom,body_temperature,blood_sugar_level,
                timestamp,longitude,latitude,alert)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """

    # non-blocking prepared CQL statement
    query = session.prepare(cql)

    # statement = SimpleStatement(query, consistency_level=ConsistencyLevel.QUORUM)
    batch = BatchStatement()
    batch.add(query, [
        str(payload.get('id')),
        str(payload.get('name')),
        int(payload.get('age')),
        str(payload.get('gender')),
        str(payload.get('phone')),
        str(payload.get('address')),
        str(payload.get('condition')),
        str(payload.get('bmi')),
        str(payload.get('status')),
        str(payload.get('device_id')),
        str(payload.get('reading_id')),
        int(payload.get('heart_rate')),
        int(payload.get('blood_pressure_top')),
        int(payload.get('blood_pressure_bottom')),
        str(payload.get('body_temperature')),
        int(payload.get('blood_sugar_level')),
        pd.to_datetime(payload.get('timestamp')),
        str(payload.get('longitude')),
        str(payload.get('latitude')),
        str(payload.get('alert'))
    ])
    session.execute(batch)
    print("Loaded Message to Database: {} " + str(payload))

async def aysnc_to_cassandra(payload):

    aiosession(session)

    query = """INSERT INTO healthcare_db.device_patient(
               id,name,age,gender,phone,address,
               condition,bmi,status,device_id,reading_id,heart_rate,
               blood_pressure_top,blood_pressure_bottom,body_temperature,blood_sugar_level,
               timestamp,longitude,latitude,alert)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
               """

    #statement = SimpleStatement(query, fetch_size=100)

    values = [
        str(payload.get('id')),
        str(payload.get('name')),
        int(payload.get('age')),
        str(payload.get('gender')),
        str(payload.get('phone')),
        str(payload.get('address')),
        str(payload.get('condition')),
        str(payload.get('bmi')),
        str(payload.get('status')),
        str(payload.get('device_id')),
        str(payload.get('reading_id')),
        int(payload.get('heart_rate')),
        int(payload.get('blood_pressure_top')),
        int(payload.get('blood_pressure_bottom')),
        str(payload.get('body_temperature')),
        int(payload.get('blood_sugar_level')),
        pd.to_datetime(payload.get('timestamp')),
        str(payload.get('longitude')),
        str(payload.get('latitude')),
        str(payload.get('alert'))
    ]
    query = await session.prepare(query, values)

    await session.execute_future(query)


async def consume_payload():
    """
    function to consume from topic and persist to database
    """

    aiosession(session)
    # create consumer object
    consumer = AIOKafkaConsumer(
        topic,
        enable_auto_commit=False,
        auto_offset_reset="earliest",
    )
    await consumer.start()

    try:
        async for message in consumer:
            payload = json.loads(message.value.decode('utf-8'))
            batch_to_cassandra(payload)
    finally:
        await consumer.stop()



if __name__ == '__main__':
    asyncio.run(consume_payload())

