# To manually run the healthcare pipeline, follow these steps:

**Step 1: Create the Docker network**
```
$ docker network create healthcare_pipeline
```

**Step 2: Compose/Build the Kafka Resources**
Go to the docker folder and run the following command:
```
$ docker-compose -f docker-compose-kafka.yaml up
```
Open a new terminal in the docker folder.

**Step 3: Compose/Build Cassandra Database**
```
$ docker-compose -f docker-compose-cassandra.yaml up -d
```

**Step 4: Connect to Cassandra**
```
$ docker exec -it cassandra cqlsh localhost 9042
```

**Step 5: Create Keyspace**
```
CREATE KEYSPACE IF NOT EXISTS healthcare_db
WITH REPLICATION = {
  'class': 'SimpleStrategy',
  'replication_factor': '3'
};
```

**Step 6: Use Keyspace**
```
USE healthcare_db;
```

**Step 7: Create Table**
```
CREATE TABLE IF NOT EXISTS healthcare_db.device_patient(
  id TEXT,
  name TEXT,
  age INT,
  gender TEXT,
  phone TEXT,
  address TEXT,
  condition TEXT,
  bmi DECIMAL,
  status TEXT,
  device_id TEXT, 
  reading_id TEXT,
  heart_rate INT,
  blood_pressure_top INT,
  blood_pressure_bottom INT,
  body_temperature DECIMAL,
  blood_sugar_level INT,
  timestamp TIMESTAMP ,
  longitude TEXT,
  latitude TEXT,
  alert TEXT,
  PRIMARY KEY ((id), timestamp))
WITH CLUSTERING ORDER BY (timestamp DESC);
```

**Step 8: Create Topic in Kafka**
```
$ docker exec -it kafka /bin/sh
$ cd /opt/kafka_2.13-2.7.0/
$ ./bin/kafka-topics.sh --create --zookeeper zookeeper:2181 --replication-factor 1 --partitions 1 --topic patient_data
$ ./bin/kafka-topics.sh --list --zookeeper zookeeper:2181
$ exit
```

**Step 9: Run the Producer & Consumer**
```
$ cd ../kafka/
$ python producer.py
$ python consumer.py
```

While the producer and consumer are running, you can check the database records:
```
SELECT COUNT(*) FROM healthcare_db.device_patient;
```

**Step 10: Run the Dashboard**
```
python dashboard.py
```

To remove everything, run the following command:
```
$ ./destroy.sh
```

Please make sure you have Docker and Docker Compose installed before proceeding with these steps.
