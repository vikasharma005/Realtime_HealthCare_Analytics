# Import required libraries

import dash_table
import pandas as pd
import numpy as np
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider



def read_cassandra(host, username, password, keyspace):
    """
    This function it is a python package that will connect to Cassandra and load the data faster

    :return: df
    """
    # patches and adds `execute_future`, `execute_futures` and `prepare_future`
    # to `cassandra.cluster.Session`
    #  cluster is the class that interact with Cassandra
    cluster = Cluster(
        contact_points=[host],
    # create the autentication
        auth_provider=PlainTextAuthProvider(username=username, password=password)
    )
    #  uses executor_threads to talk to cassndra driver
    session = cluster.connect()
    session.set_keyspace(keyspace)

    #prepare query for cassandra to read the data
    query = 'SELECT * FROM healthcare_db.device_patient'

    #store the data in query to dataframe
    df = pd.DataFrame(session.execute(query))

    return df


# -- These are the counts for the blue
def get_total_counts(df):
    """
    This function will get the the total of patients, reading, alerts, emergencies and warnings
    :param df:
    :return: total_patients, total_readings, total_alerts, total_emergencies, total_warnings
    """

    # filter the dataframe to just id, reading_id and alert
    df2 = df[['id', 'reading_id', 'alert']]

    # Group the age segment by unique names (in case of each patient has more than one record) to count the specific segments
    total_patients = df2['id'].nunique()
    total_readings = df2['reading_id'].nunique()

    # Remove Null or Nan values in Alert Column
    df2 = df2[df2['alert'].notna()]

    # Get count of alerts where alert contains EMERGENCY!
    total_emergencies = df2['alert'][df2['alert'].str.contains('EMERGENCY!')].count()

    # Get count of alerts where alert contains WARNINGS!
    total_warnings = df2['alert'][df2['alert'].str.contains('WARNING!')].count()
    # get the sum of all alerts, that contains warning and emergencies
    total_alerts = total_emergencies + total_warnings

    return total_patients, total_readings, total_alerts, total_emergencies, total_warnings


# -- These are the counts for the alert count
def get_alert_counts(df):
    """
    This function will get the total of alerts based on each condition
      :return:hypertension, hypothermia, hyperthermia, fever, hyperglycemia, tachycardia
    """
    alerts = create_alert_table(df)
    alerts = alerts[['alert']]
    # Get count of alerts where alert contains HYPERTENSION!
    hypertension = alerts['alert'][alerts['alert'].str.contains('HYPERTENSION')].count()
    # Get count of alerts where alert contains HYPOTHERMIA!
    hypothermia = alerts['alert'][alerts['alert'].str.contains('HYPOTHERMIA')].count()
    # Get count of alerts where alert contains HYPERTHERMIA!
    hyperthermia = alerts['alert'][alerts['alert'].str.contains('HYPERTHERMIA')].count()
    # Get count of alerts where alert contains FEVER!
    fever = alerts['alert'][alerts['alert'].str.contains('FEVER')].count()
    # Get count of alerts where alert contains HYPERGLYCEMIA!
    hyperglycemia = alerts['alert'][alerts['alert'].str.contains('HYPERGLYCEMIA')].count()
    # Get count of alerts where alert contains TACHYCARDIA!
    tachycardia = alerts['alert'][alerts['alert'].str.contains('TACHYCARDIA')].count()

    return hypertension, hypothermia, hyperthermia, fever, hyperglycemia, tachycardia


# -- This filters the table for ALERTS
def create_alert_table(df):
    """
    This funcion will filter the alerts for the tables
    :param df:
    :return: df
    """
    # keep only the columns we need
    df = df[['timestamp','name', 'phone', 'alert', 'latitude', 'longitude']]

    # select/slice from the dataframe where alert does not equal '' (is not empty)
    df = df[df['alert'] != 'None']
    df = df[df['alert'] != '']

    conditions = [(df['alert'].str.contains("EMERGENCY")), (df['alert'].str.contains("WARNING"))]

    values = ['Emergency', 'Warning']
    df["type"] = np.select(conditions, values)
    
    return df


# -- This creates the alert graph for dash on the dashboard
def create_alert_graph(df):
    """
    This function Create Dash datatable from Pandas DataFrame.
    :return: table
    """

    df = create_alert_table(df)

    df = df.sort_values('timestamp', ascending=False)
    df['timestamp'] = df['timestamp'].dt.strftime('%Y-%m-%d %H:%M')

    # Update the columns to have capital letter as first letter
    df.columns = df.columns.str.title()
    
    table = dash_table.DataTable(
        id='alert-table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        sort_action="native",
        style_table={'overflowX': 'auto'},
        style_data={'font-family': 'Open Sans'},
        sort_mode='single',
        page_size=20,
        style_header={
        'backgroundColor': '#404e68',
        'color':'#FFFFFF',
        'font-size': '16px',
          'font-family': 'Open Sans',

    },
    style_data_conditional=[
        {
            'if': {
                'filter_query': '{{Type}} = {}'.format('Emergency'),

            },
            'backgroundColor': '#FFFFFF',
            'color': '#be1558'
        },#fff586
        {
            'if': {
                'filter_query': '{{Type}} = {}'.format('Warning'),

            },
            'backgroundColor': '#FFFFFF',
            'color': '#434343'
        }
        ]
    )
    return table


# -- Functions to generate the Dropdown Pie Chart Data -- #
def get_bmi_segment(df):
    """
    This funcion will generate the chart for the bmi segment
    :param df:
    :return:bmi_segments
    """

    # filter the dataframe to just names and bmi
    bmis = df[['name', 'bmi']]

    # create a list of our conditions
    conditions = [
        (bmis['bmi'] < 18.5),
        (bmis['bmi'] > 18.5) & (bmis['bmi'] <= 25),
        (bmis['bmi'] > 25) & (bmis['bmi'] <= 30),
        (bmis['bmi'] > 30) & (bmis['bmi'] <= 35),
        (bmis['bmi'] > 35)
    ]

    # create a list of the values we want to assign for each condition
    values = ['Underweight 18', 'Normal', 'Overweight', 'Obese', 'Extremely Obese']

    # create a new column and use np.select to assign values to it using our lists as arguments
    bmis['bmi_segment'] = np.select(conditions, values)

    # Group the age segment by unique names (as each patient has more than one record) to count the age segments
    bmi_segments = bmis.groupby('bmi_segment')['name'].nunique()

    return bmi_segments


def get_existing_segments(df, segment):
    """
    This funcion will filter the data frame and get only name and age
    :param df:
    :param segment: string (age, status, condition, bmi, gender)
    :return:series
    """

    # filter the dataframe to just names and ages
    df2 = df[['name', segment]]

    # Group the age segment by unique names (as each patient has more than one record) to count the specific segments
    series = df2.groupby(segment)['name'].nunique()

    return series


def get_age_segment(df):
    """
     This funcion will filter the data frame and get only age
    :param df:
    :return:age_segments
    """

    # filter the dataframe to just names and ages
    ages = df[['name', 'age']]

    # create a list of our conditions
    conditions = [
        (ages['age'] < 18),  # 1
        (ages['age'] >= 18) & (ages['age'] <= 39),  # 2
        (ages['age'] >= 40) & (ages['age'] <= 49),  # 3
        (ages['age'] >= 50) & (ages['age'] <= 59),  # 4
        (ages['age'] >= 60) & (ages['age'] <= 69),  # 5
        (ages['age'] >= 70) & (ages['age'] <= 79),  # 6
        (ages['age'] >= 80) # 7
    ]

    # create a list of the values we want to assign for each condition
    values = ['Below 18',  # 1
              '18 to 39',  # 2
              '40 to 49',  # 3
              '50 to 59',  # 4
              '60 to 69',  # 5
              '70 to 79',  # 6
              'Over 80']   # 7

    # create a new column and use np.select to assign values to it using our lists as arguments
    ages['age_segment'] = np.select(conditions, values)
    print(ages)
    # Group the age segment by unique names (as each patient has more than one record) to count the age segments
    age_segments = ages.groupby('age_segment')['name'].nunique()

    return age_segments


def get_postcode_segment(df):
    """
    This funcion will filter the data frame and get only name and address
    :return: series
    """
    # filter the dataframe to just names and address
    df = df[['name', 'address']]
    # concatinate the name and address
    df = pd.concat([df[["name"]], df["address"].str.split(',', expand=True)], axis=1)
    df = df[["name", 1]]
    df.columns = ['name', 'postcode']

    # Group the age segment by unique names (as each patient has more than one record) to count the specific segments
    series = df.groupby('postcode')['name'].nunique()

    return series


def filter_dataframe(df, disease, status, age, gender,
                     bmi, temperature, heartrate, bloodsugar, systolic, diastolic):
    """
    This function will filter the dataframe to get the parameters that were inputted
     :return:  filtered_data
    """
    filtered_data = df[
        # Filter by diseases/conditions
        (df["condition"].isin(disease))
        # Filter by status
        & (df["status"].isin(status))
        # Filter by gender
        & (df["gender"].isin(gender))
        # Filter between ages
        & (df["age"] >= age[0]) & (df["age"] <= age[1])
        # Filter by BMI
        & (df["bmi"] >= bmi[0]) & (df["bmi"] <= bmi[1])
        # Filter between heart rate
        & (df["heart_rate"] >= heartrate[0]) & (df["heart_rate"] <= heartrate[1])
        # Filter between body temperature
        & (df["body_temperature"] >= temperature[0]) & (df["body_temperature"] <= temperature[1])
        # Filter between blood sugar
        & (df["blood_sugar_level"] >= bloodsugar[0]) & (df["blood_sugar_level"] <= bloodsugar[1])
        # Filter between blood pressure top (systolic)
        & (df["blood_pressure_top"] >= systolic[0]) & (df["blood_pressure_top"] <= systolic[1])
        # Filter between blood pressure bottom (diastolic)
        & (df["blood_pressure_bottom"] >= diastolic[0]) & (df["blood_pressure_bottom"] <= diastolic[1])
        ]

    # keep only the columns that are necessary
    filtered_data = filtered_data[['name', 'condition', 'reading_id',
                                   'heart_rate', 'blood_pressure_top', 'blood_pressure_bottom', 'body_temperature',
                                   'blood_sugar_level', 'timestamp', 'longitude', 'latitude']]

    return filtered_data


def produce_health_stats(df, name):
    """
    This function will generate the data to get the health status for each patient

    :return: index, timestamp, heart_rate, body_temperature, blood_sugar
    """
    try:
        df["name"] == name
    except:
        return None, None, None, None

    index = list(df.index.values)
    heart_rate = df.loc[df['name'] == name]["heart_rate"].tolist()
    body_temperature = df.loc[df['name'] == name]["body_temperature"].tolist()
    blood_sugar = df.loc[df['name'] == name]["blood_sugar_level"].tolist()
    timestamp = df.loc[df['name'] == name]["timestamp"].tolist()

    return index, timestamp, heart_rate, body_temperature, blood_sugar


def produce_blood_pressure(df, name):
    try:
        df["name"] == name
    except:
        return None, None, None, None

    index = list(df.index.values)
    blood_pressure_top = df.loc[df['name'] == name]["blood_pressure_top"].tolist()
    blood_pressure_bottom = df.loc[df['name'] == name]["blood_pressure_bottom"].tolist()
    timestamp = df.loc[df['name'] == name]["timestamp"].tolist()

    return index, timestamp, blood_pressure_top, blood_pressure_bottom
