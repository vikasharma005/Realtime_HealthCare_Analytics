
<p align="center">
  <img src="https://raw.githubusercontent.com/vikasharma005/Realtime_HealthCare_Analytics/master/assets/dash.png">
</p>


# About


## Modules Used
* aiokafka - Asynchronous Kafka Streaming
* asyncio - Asynchronous Python Threading
* aiomysl 
* cassandra-driver - Cassandra Connector/Sink
* aiocassandra - Asynchronous Cassandra Writing


# Demonstration
The following are screenshots for the app in this repo.

Main Dashboard & Callback Graph Navigation:
![alt text](https://raw.githubusercontent.com/vikasharma005/Realtime_HealthCare_Analytics/master/diagrams/screencaptures/main.gif "Systems Architecture for Project")

Alert Table:
![alt text](https://raw.githubusercontent.com/vikasharma005/Realtime_HealthCare_Analytics/master/diagrams/screencaptures/dash_table.gif "Systems Architecture for Project")

Sensor Reading Map:
![alt text](https://raw.githubusercontent.com/vikasharma005/Realtime_HealthCare_Analytics/master/diagrams/screencaptures/map.gif "Systems Architecture for Project")

Filtering the Map:
![alt text](https://raw.githubusercontent.com/vikasharma005/Realtime_HealthCare_Analytics/master/diagrams/screencaptures/changes.gif "Systems Architecture for Project")

Heart Rate, Body Temperature and Bloog Sugar Graphs:
![alt text](https://raw.githubusercontent.com/vikasharma005/Realtime_HealthCare_Analytics/master/diagrams/screencaptures/health_stats.gif "Systems Architecture for Project")


Blood Pressure Graphs:

![alt text](https://raw.githubusercontent.com/vikasharma005/Realtime_HealthCare_Analytics/master/diagrams/screencaptures/bloodpressure.gif "Systems Architecture for Project")

All Patient Stats:
![alt text](https://raw.githubusercontent.com/vikasharma005/Realtime_HealthCare_Analytics/master/diagrams/screencaptures/pie_charts.gif "Systems Architecture for Project")

# Project Diagrams
To view diagrams and schematics for the project please view this link: https://github.com/vikasharma005/Realtime_HealthCare_Analytics/tree/master/diagrams


# Installation

## Clone Repo


## Setup Prerequisities

## Install Docker

## Install Docker-compose
$ sudo curl -L "https://github.com/docker/compose/releases/download/1.26.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

$ sudo chmod +x /usr/local/bin/docker-compose

$ docker–compose -–version

## Install requirements


# Running Project

## Deployment/Destroy Clusters + APP

### Deploy Script

$ ./deploy.sh

### Destroy Script

$ ./destory.sh


## MANUAL TEAR DOWN STEPS

### start main docker compose
$ docker network create healthcare_pipeline

$ docker-compose -f docker-compose-kafka.yaml up -d --remove-orphans

$ docker-compose -f docker-compose-kafka.yaml logs -f broker | grep "started"

$ docker-compose -f docker-compose-cassandra.yaml up -d --remove-orphans

$ docker-compose up --build


## INTERFACING WITH APP
### View Stream in Topic
$ docker-compose -f docker-compose-kafka.yaml exec broker kafka-console-consumer --bootstrap-server localhost:9092 --topic queueing.healthcare --from-beginning

### View Data via Cassandra Shell

#### Connect to Cassandra Shell
$ docker exec -it cassandra cqlsh localhost 9042 


##### Cassandra shell commands
cqlsh> use healthcare_db;

cqlsh:healthcare_db> select * from healthcare_db.device_patient;

 id | content | type
----+---------+------

(0 rows)

cqlsh:healthcare_db> exit


## MANUAL TEAR DOWN STEPS

### Stop the App
$ docker-compose down --remove-orphans

### Stop the Kafka cluster
$ docker-compose -f docker-compose-kafka.yaml stop

### Remove Contents of Topics and Kafka cluster
$ docker-compose -f docker-compose-kafka.yaml down

### Stop Cassandra DB
$ docker-compose -f docker-compose-cassandra.yaml down
$ docker rm container cassandra


### Remove Docker network
$ docker network rm healthcare_pipeline


# Testing


# Outstanding TODO/Issues

#   R e a l t i m e _ H e a l t h C a r e _ A n a l y t i c s 
 
 
