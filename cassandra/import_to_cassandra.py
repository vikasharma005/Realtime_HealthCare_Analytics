from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import pandas as pd
from time import time
from decimal import Decimal


def pandas_factory(colnames, rows):
    return pd.DataFrame(rows, columns=colnames)

cluster = Cluster(
    contact_points=['127.0.0.1'],
    auth_provider = PlainTextAuthProvider(username='cassandra', password='cassandra')
)
session = cluster.connect()
session.set_keyspace('healthcare_db')
session.row_factory = pandas_factory
session.default_fetch_size = 10000000 #needed for large queries, otherwise driver will do pagination. Default is 50000.


def import_cassandra():
    session = cluster.connect()
    session.set_keyspace('healthcare_db')


    prepared = session.prepare("""
            INSERT INTO healthcare_db.device_patient(id,name,age,gender,phone,address,
            condition,bmi,status,device_id,reading_id,heart_rate,
            blood_pressure_top,blood_pressure_bottom,body_temperature,blood_sugar_level,
            timestamp,longitude,latitude,alert)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """)
    from csv import reader

    with open("../test_data/test_full_data.csv", "r") as data:
        csv_reader = reader(data)
        header = next(csv_reader)
        if header != None:
            for row in csv_reader:
                print(row)
                id =row[0]
                name = row[1]
                age = int(row[2])
                gender= row[3]
                phone= row[4]
                address= row[5]
                condition= row[6]
                bmi= Decimal(row[7])
                status= row[8]
                device_id= row[9]
                reading_id= row[10]
                heart_rate= int(row[11])
                blood_pressure_top= int(row[12])
                blood_pressure_bottom= int(row[13])
                body_temperature = Decimal(row[14])
                blood_sugar_level= int(row[15])
                timestamp= pd.to_datetime(row[16])
                longitude= row[17]
                latitude= row[18]
                alert = row[19]


                session.execute(prepared, [
                    id, name, age, gender, phone, address, condition, bmi, status, device_id, reading_id, heart_rate,
                    blood_pressure_top, blood_pressure_bottom, body_temperature,blood_sugar_level, timestamp, longitude,
                    latitude, alert

                ])

    #closing the file
    data.close()

    #closing Cassandra connection
    session.shutdown()

import_cassandra()