import os
import random
import json
import asyncio
from aiokafka.producer import AIOKafkaProducer
import generator
import datetime

#Configuration
topic =  'patient_data'
#kafka_broker_url = os.environ.get('KAFKA_BROKER_URL')
kafka_broker_url = 'localhost:9092'

def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

def serializer(data):
    """
    function to serialize dict to json
    """
    return json.dumps(data, default=myconverter).encode()


async def produce_payload():
    """
    function to transform payload and batch append to kafka producer
    """
    # Get variables and arrays(lists) from the generator
    patient_count = generator.patient_count
    timestamps = generator.create_time_of_measurement()

    producer = AIOKafkaProducer()
    await producer.start()

    batch = producer.create_batch()

    # for every iteration in patient count
    for i in range(patient_count):
        print("Generating Patient Data for {0} patients".format(patient_count))
        # create the patient content payload
        patient: dict = generator.create_patient_content()
        for timestamp in timestamps:
            # create the sensor content payload
            sensor: dict = generator.create_sensor_content(timestamp)
            # Create the emergency alert content
            emergency = generator.create_emergency_alerts(patient, sensor)
            # join the patient, sensor and emergency data using ** operator
            records: dict = {**patient, **sensor, **emergency}
            # serialize (compress) the records to send quickly
            serialized = serializer(records)

            metadata = batch.append(key=None, value=serialized, timestamp=None)
            if metadata is None:
                partitions = await producer.partitions_for(topic)
                partition = random.choice(tuple(partitions))
                await producer.send_batch(batch, topic, partition=partition)
                print("%d messages sent to partition %d"
                      % (batch.record_count(), partition))
                batch = producer.create_batch()

    partitions = await producer.partitions_for(topic)
    partition = random.choice(tuple(partitions))
    await producer.send_batch(batch, topic, partition=partition)
    print("%d messages sent to partition %d"
          % (batch.record_count(), partition))
    await producer.stop()

if __name__ == '__main__':
    asyncio.run(produce_payload())


