
#!/bin/bash
cd ./docker
# Stop the App
echo "--- Tear Down Started --- "
echo -n "Stop the App"
sudo docker-compose down

# Stop the Kafka cluster
echo "Stop the Kafka cluster"
sudo docker-compose -f docker-compose-kafka.yaml stop

# Remove Contents of Topics and Kafka cluster
echo "Remove Contents of Topics and Kafka cluster"
sudo docker-compose -f docker-compose-kafka.yaml down

# Stop Database
echo "Stopping Cassandra Instance"
sudo docker-compose -f docker-compose-cassandra.yaml down

echo "Removing Cassandra & Keyspace Containers"
sudo docker rm cassandra
sudo docker rm /cassandra-keyspace

echo "Removing Cached Data on Cassandra Volume"
sudo rm -rf ../cassandra/db/


# Remove Docker network
echo "Remove Docker network"
sudo docker network rm healthcare_pipeline

echo "Remove any orphan containers"
sudo docker-compose down --remove-orphans

echo "--- Tear Down Complete --- "
