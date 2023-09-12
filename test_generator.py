import pytest
from kafka import generator as generator
import datetime

patient_payload_sample = {
    "id" : 1,
    "name": "test person",
    "age":34,
    "gender" : "Female",
    "phone": "+353-88-3658730",
    "address" : "87591 Angel Pines Suite 496,Dublin 3, Dublin, Republic of Ireland",
    "condition": "hypertension",
    "bmi": 26.43,
    "status": "critical unhealthy",
    "device_id": "SMARTWATCH3-372788e3655e4f73ad6427c517d97d8c"
}

sensor_payload_sample = {
    "reading_id": "26d537f50a294c77af90b7cfb9d38e5f",
    "heart_rate": 132,
    "blood_pressure_top" : 167,
    "blood_pressure_bottom": 111,
    "body_temperature":37.15,
    "blood_sugar_level" :119,
    "timestamp" : "2021-08-04 22:11:00",
    "longitude": -6.315947,
    "latitude": 53.364602
}



def test_generate_seed():
    """
    This test asserts that the generate_seed function output is less than/equal to 100.
    """
    assert generator.generate_seed() <= 100


def test_unique_id():
    """
    This test asserts that the create_unique_id  function is an instance of the type string.
    """
    assert isinstance(generator.create_unique_id(), str)


def test_create_device_id():
    """
     This test asserts that the create_device_id  function is an instance of the type string.
    """
    assert isinstance(generator.create_device_id(), str)


def test_create_heart_rate():
    """"
    This test asserts that the create_heart_rate function output is greater
    than/equal to 40 and less than/equal to 219 when the parameter/input
    emergency is set to False.
    """
    assert 40 <= generator.create_heart_rate(emergency=False) <= 219


def test_emergency_heart_rate():
    """
    This test asserts that the create_heart_rate function output is greater
    than/equal to 40 and less than/equal to 300 when the parameter/input
    emergency is set to True.
    """
    assert 40 <= generator.create_heart_rate(emergency=True) <= 300


def test_blood_pressure_top():
    """
    This test asserts that the create_blood_pressure_top   function output is greater than/equal to
    100 and less than/equal to 179 when the parameter/input
    emergency is set to True.
    """
    assert 100 <= generator.create_blood_pressure_top(emergency=False) <= 179



def test_emergency_blood_pressure_top():
    """
    This test asserts that the create_emergency_blood_pressure_top  function output is greater than/equal
    to 100 and less than/equal to 200 when the parameter/input
    emergency is set to True.
    """
    assert 100 <= generator.create_blood_pressure_top(emergency=True) <= 220


def test_blood_pressure_bottom():
    """
    This test asserts that the create_blood_pressure_bottom  function output is greater than/equal to 50 and less than/equal
    to 119 when the parameter/input emergency is set to False.

    """
    assert 50 <= generator.create_blood_pressure_bottom(emergency=False) <= 119



def test_emergency_blood_pressure_bottom():
    """
    This test asserts that the create_emergency_blood_pressure_bottom  function output
    is greater than/equal to 50 and less than/equal to 140 when the parameter/input
    emergency is set to True.
    """
    assert 50 <= generator.create_blood_pressure_bottom(emergency=True) <= 140


def test_body_temperature():
    """
    This test asserts that the create_body_temperature     function output is greater than/equal to 35.0 and
    less than/equal to 37.3 when the parameter/input emergency is set to False.
     """
    assert 35.0 <= generator.create_body_temperature(emergency=False) <= 37.3


def test_emergency_body_temperature():
    """
    This test asserts that the create_emergency_body_temperature   function output is greater than/equal to 35.0
    and less than/equal to 41.9 when the parameter/input emergency is set to True
    """
    assert 35.0 <= generator.create_body_temperature(emergency=True) <= 41.9


def test_blood_sugar_level():
    """
    This test asserts that the create_blood_sugar_level  function output is greater
    than/equal to 35 and less than/equal to 199  when the parameter/input emergency is set to False.
    """
    assert 35 <= generator.create_blood_sugar_level(emergency=False) <= 199


def test_emergency_blood_sugar_level():
    """
    This test asserts that the create_emergency_blood_sugar_level   function output is greater than/equal to 35 and less than/equal
    to 400 when the parameter/input emergency is set to True.
    """
    assert 35 <= generator.create_blood_sugar_level(emergency=True) <= 400


def test_phone_number():
   """
   This test asserts that the prefix +353 is a string of the function create_phone_number.
   """
   assert '+353-' in str(generator.create_phone_number())


def test_geolocation_longitude():
    """
    This test asserts that the create_geolocation_longitude   function output is greater than/equal to -6.44 and less than/equal to -6.20
    """
    assert -6.44 <= generator.create_geolocation('longitude') <= -6.20


def test_geolocation_latitude():
    """
    This test asserts that the create_geolocation_latitude  function output is greater than/equal to 53.20 and less than/equal to 53.40
    """
    assert 53.20 <= generator.create_geolocation('latitude') <= 53.40


def test_dublin_address():
    """
    This test asserts that the Dublin, Republic of Ireland is a string of the function create_dublin_address.
    """
    assert ', Dublin, Republic of Ireland' in str(generator.create_dublin_address())


def test_health_status():
    """
    This test asserts that the function create_health_status is present in the array conditions and status that were created.
    It also checks if the bmi than/equal to 18.5 and less than/equal to 40.5
    """
    conditions = ['diabetes', 'hypertension', 'heart disease', 'none']
    statuses = ['critical unhealthy', 'stable unhealthy', 'stable healthy', 'emergency']

    # Loop it time times so we pick random conditions, statues and BMI for the patient_health to check
    for x in range(10):
        patient_health = generator.create_health_status()
        actual_condition = patient_health[0]
        actual_bmi = patient_health[1]
        actual_status = patient_health[2]

        assert actual_condition in conditions
        assert 18.5 <= actual_bmi <= 40.5
        assert actual_status in statuses


def test_time_of_measurement():
    actual_timestamps = generator.create_time_of_measurement()

    #Test if the output is a list
    assert isinstance(actual_timestamps, list)
    #Test that an element in the list is datetime format
    assert isinstance(actual_timestamps[0], datetime.date)


def test_patient_content():
    """
    This test asserts if the column of the patient content are part of the function
    create_patient_content.
    """
    payload = generator.create_patient_content()
    columns = ['id',
                 'name',
                 'age',
                 'gender',
                 'phone',
                 'address',
                 'condition',
                 'bmi',
                 'status',
                 'device_id']
    for column in columns:
        assert column in payload.keys()


def test_sensor_content():
    """
    This test asserts if the column of the sensor content are part of the function
    create_sensor_content.
    """
    payload = generator.create_sensor_content(timestamp='2021-08-04 22:17:00')
    columns = ['reading_id',
              'heart_rate',
              'blood_pressure_top',
              'blood_pressure_bottom',
              'body_temperature',
              'blood_sugar_level',
              'timestamp',
              'longitude',
              'latitude']
    for column in columns:
        assert column in payload.keys()


def test_emergency_alerts_payload():
    """
    This test asserts if the column emergency are part of the function
    create_emergency_alerts.
    :return:
    """
    patient_payload = generator.create_patient_content()
    sensor_payload = generator.create_sensor_content(timestamp='2021-08-04 22:17:00')

    payload = generator.create_emergency_alerts(patient_payload,sensor_payload)
    column = 'alert'

    assert column in payload.keys()


def test_emergency_condition_one():
    """
    This function will test if condition one, 'EMERGENCY! HYPERTENSION DETECTED,
    from create_emergency_alerts() is part the string alert payload.
    """
    alert_payload = generator.create_emergency_alerts(patient_payload_sample,
                                      sensor_payload_sample)

    assert 'EMERGENCY! HYPERTENSION DETECTED' in str(alert_payload)


def test_emergency_condition_two():
    """
    This function will test if condition two body temperature equals 34 and the message EMERGENCY! HYPOTHERMIA DETECTED
    from create_emergency_alerts() is part the string alert payload.
    """
    sensor_payload_sample["body_temperature"] = 34
    alert_payload = generator.create_emergency_alerts(patient_payload_sample,
                                      sensor_payload_sample)

    assert 'EMERGENCY! HYPOTHERMIA DETECTED' in str(alert_payload)


def test_emergency_condition_three():
    """
    This function will test if condition two body temperature equals 42 and the message EMERGENCY! HYPERTHERMIA DETECTED
    from create_emergency_alerts() is part the string alert payload.
    :return:
    """
    sensor_payload_sample["body_temperature"] = 42
    alert_payload = generator.create_emergency_alerts(patient_payload_sample,
                                                      sensor_payload_sample)

    assert 'EMERGENCY! HYPERTHERMIA DETECTED' in str(alert_payload)


def test_emergency_condition_four():
    """
    This function will test if condition four,body temperature equals 39 and the status is stable unhealthy , then
    the message to be printed is WARNING! FEVER DETECTED from create_emergency_alerts()
    is part the string alert payload.
    """
    sensor_payload_sample["body_temperature"] = 39
    patient_payload_sample["status"] = "stable unhealthy "
    alert_payload = generator.create_emergency_alerts(patient_payload_sample,
                                                      sensor_payload_sample)

    assert 'WARNING! FEVER DETECTED' in str(alert_payload)


def test_emergency_condition_five():
    """
    This function will test if condition five,blood sugar level equals 350 and the condition is diabetes, then
    the message to be printed is EMERGENCY! HYPERGLYCEMIA DETECTED from create_emergency_alerts()
    is part the string alert payload.
    """
    sensor_payload_sample["blood_sugar_level"] = 350
    patient_payload_sample["condition"] = "diabetes"
    alert_payload = generator.create_emergency_alerts(patient_payload_sample,
                                                      sensor_payload_sample)

    assert 'EMERGENCY! HYPERGLYCEMIA DETECTED' in str(alert_payload)


def test_emergency_condition_six():
    """
    This function will test if condition six,bheart_rate equals 290 and the condition is heart disease, then
    the message to be printed is WARNING! TACHYCARDIA DETECTED from create_emergency_alerts()
    is part the string alert payload.
    :return:
    """
    sensor_payload_sample["heart_rate"] = 290
    patient_payload_sample["condition"] = "heart disease"
    alert_payload = generator.create_emergency_alerts(patient_payload_sample,
                                                      sensor_payload_sample)

    assert 'WARNING! TACHYCARDIA DETECTED' in str(alert_payload)
