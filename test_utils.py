import pytest
from pandas._testing import assert_frame_equal, assert_series_equal
import pathlib
import pandas as pd

# get relative test_data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("test_data").resolve()

from utils import functions as utils
from utils import config as config

# Load test data files to create them as input dataframes
df_input = pd.read_csv(str(DATA_PATH) + "/test_full_data.csv")
df_input1 = pd.read_csv(str(DATA_PATH) + "/test_data1.csv")
df_input2 = pd.read_csv(str(DATA_PATH) + "/test_data2.csv")
df_input3= pd.read_csv(str(DATA_PATH) + "/test_data3.csv")
df_input4 = pd.read_csv(str(DATA_PATH) + "/test_data4.csv")


def test_read_cassandra():
    pass


def test_get_total_counts():

    """
    This function will call all get total counts funcion an test if the total of patients,
    readings, alerts, emergencies and warnings are as expected.
     """
    # call the get_total_counts function by passing test_df_1 and store the results as the variables
    patients, readings, alerts, emergencies, warnings = utils.get_total_counts(df_input1)

    assert patients == 100  # We expect to have 100 patients
    assert readings == 2981  # We expect to have 2981 sensor readings
    assert alerts == 2981  # We expect to have 2981 total alerts
    assert emergencies == 2044  # We expect to have 2044 emergency alerts
    assert warnings == 937  # We expect to have 2044 warning alerts


def test_get_alert_counts():
    """
    This function will call all get total counts funcion an test if the total of hypertension, hypothermia,
    hyperthermia, fever, hyperglycemia and tachycardia are as expected.
    """
    hypertension, hypothermia, hyperthermia, fever, hyperglycemia, tachycardia = utils.get_alert_counts(df_input1)

    assert hypertension == 185
    assert hypothermia == 642
    assert hyperthermia == 1
    assert fever == 936
    assert hyperglycemia == 1216
    assert tachycardia == 1


def test_create_alert_table_instance():
    """
    This funcion will test that the object returned (df) by the function is a dataframe (isinstance)
    """

    # Run the function with the input data csv to create the dataframe from the create_alert_table function
    actual_df = utils.create_alert_table(df_input2)

    assert isinstance(actual_df, pd.DataFrame)


def test_create_alert_table_columns():
    """
    This funcion will test that the columns returned are timestamp, name, phone, alert, latitude, longitude
    """

    # load result data file as a dataframe. We use these to test the dataframe functions output matches the input
    expected_df = pd.read_csv(str(DATA_PATH) + "/result_data2.csv")

    # Run the function with the input data csv to create the dataframe from the create_alert_table function
    actual_df = utils.create_alert_table(df_input2)
    expected_columns = ["timestamp", "name", "phone", "alert", "latitude", "longitude"]
    actual_columns = list(actual_df.head()) # convert the columns/head of actual_df to a list to compare to expected

    assert actual_columns == expected_columns


def test_create_alert_table_matching():
    """
    This funcion will test that the actual dataframe matches the expected dataframe
    :return:
    """
    # load result data file as a dataframe. We use these to test the dataframe functions output matches the input
    expected_df = pd.read_csv(str(DATA_PATH) + "/result_data2.csv")

    # Run the function with the input data csv to create the dataframe from the create_alert_table function
    actual_df = utils.create_alert_table(df_input2)
    # use pandas testing to assert dataframes equal
    assert_frame_equal(actual_df, expected_df)


def test_filter_dataframe_instance():
    """
    This funcion will test that the object returned (df) by the function is a dataframe (isinstance)
    :return:
    """
    # -------- Test 1 -------- #
    # generate a filtered dataframe
    actual_df = utils.filter_dataframe(df=df_input, disease=config.diseases,
                                       status=config.statuses,
                                       age=[50, 90],
                                       gender=config.genders,
                                       bmi=[19, 30], temperature=[34.0, 36.9], heartrate=[40, 200],
                                       bloodsugar=[35, 200],
                                       systolic=[100, 140], diastolic=[40, 100])

    assert isinstance(actual_df, pd.DataFrame)


def test_filter_dataframe_matching_one():
    """
    This funcion will test that the object returned (df) by the function is a dataframe (isinstance) matches with the input

    :return:
    """

    # load result data file as a dataframe. We use these to test the dataframe functions output matches the input
    expected_df = pd.read_csv(str(DATA_PATH) + "/result_data3.csv")

    # all diseases, all statuses, all genders, old ages and high readings
    actual_df = utils.filter_dataframe(df=df_input, disease=config.diseases,
                                       status=config.statuses,
                                       age=[50, 90],
                                       gender=config.genders,
                                       bmi=[19, 30], temperature=[34.0, 36.9], heartrate=[40, 200],
                                       bloodsugar=[35, 200],
                                       systolic=[100, 140], diastolic=[40, 100])

    # Drop indexes (we don't want to compare indexes, only the values of the dataframe)
    actual_df.reset_index(drop=True, inplace=True)
    expected_df.reset_index(drop=True, inplace=True)

    assert_frame_equal(actual_df, expected_df)


def test_filter_dataframe_matching_two():
    """
    This function will test that the object returned (df) by the function is a data frame (isinstance) matches with the input
    :return:
    """
    # load result data file as a dataframe. We use these to test the dataframe functions output matches the input
    expected_df = pd.read_csv(str(DATA_PATH) + "/result_data4.csv")

    # specific diseases, specific statuses, males, old ages and mixed readings
    actual_df = utils.filter_dataframe(df=df_input,
                                       disease=['diabetes', 'hypertension'],
                                       status=['stable unhealthy', 'stable healthy'],
                                       age=[50, 90],
                                       gender=['Male'],
                                       bmi=[19, 30], temperature=[37.0, 41.8], heartrate=[40, 200],
                                       bloodsugar=[35, 200],
                                       systolic=[100, 140], diastolic=[100, 150])

    # Drop indexes (we don't want to compare indexes, only the values of the dataframe)
    actual_df.reset_index(drop=True, inplace=True)
    expected_df.reset_index(drop=True, inplace=True)

    assert_frame_equal(actual_df, expected_df)


def test_filter_dataframe_matching_three():
    """
    This function will test that the object returned (df) by the function is a data frame (isinstance) matches with the input.
    :return:
    """

    # load result data file as a dataframe. We use these to test the dataframe functions output matches the input
    expected_df = pd.read_csv(str(DATA_PATH) + "/result_data5.csv")

    # specific diseases, specific statuses, females, young ages and mixed readings
    actual_df = utils.filter_dataframe(df=df_input,
                                       disease=['diabetes', 'hypertension', 'heart disease'],
                                       status=['stable unhealthy', 'stable healthy', 'critical unhealthy'],
                                       age=[50, 90],
                                       gender=['Female'],
                                       bmi=[30, 40], temperature=[34.0, 36.9], heartrate=[200, 300],
                                       bloodsugar=[200, 400],
                                       systolic=[140, 220], diastolic=[40, 100])

    # Drop indexes (we don't want to compare indexes, only the values of the dataframe)
    actual_df.reset_index(drop=True, inplace=True)
    expected_df.reset_index(drop=True, inplace=True)

    assert_frame_equal(actual_df, expected_df)


def test_get_bmi_segment():
    """
    This function will test that the expected series returned matches with the expected data

    :return:
    """

    #Prepare the expected data as a Pandas Series
    expected_data = {'Extremely Obese': 24, 'Normal': 32, 'Obese': 30, 'Overweight': 14}

    expected_series = pd.Series(data=expected_data,
                                index=['Extremely Obese', 'Normal', 'Obese', 'Overweight'])
    # Run the get_bmi_sgement function to return the actual series
    actual_series = utils.get_bmi_segment(df_input)

    # Compare actual vs expected
    assert_series_equal(actual_series,expected_series, check_names=False)


def test_get_age_segment():
    """
    This function will test that the expected series returned matches with the expected data
    """

    #Prepare the expected data as a Pandas Series
    expected_data = {'18 to 39': 44, '40 to 49': 14, '50 to 59': 25, '60 to 69': 17}

    expected_series = pd.Series(data=expected_data,
                                index=['18 to 39', '40 to 49', '50 to 59', '60 to 69'])
    # Run the get_bmi_sgement function to return the actual series
    actual_series = utils.get_age_segment(df_input)

    # Compare actual vs expected
    assert_series_equal(actual_series,expected_series, check_names=False)


def test_get_existing_gender_segments():
    """
    This function will test that the expected series returned matches with the expected data that is female and male

    :return:
    """
    #Prepare the expected data as a Pandas Series
    expected_data = {'Female': 47, 'Male': 53}

    expected_series = pd.Series(data=expected_data,
                                index=['Female', 'Male'])
    # Run the get_bmi_sgement function to return the actual series
    actual_series = utils.get_existing_segments(df_input, 'gender')

    # Compare actual vs expected
    assert_series_equal(actual_series,expected_series, check_names=False)


def test_get_existing_health_segments():
    """
    This function will test that the expected series returned matches with the expected data
    that is critical unhealthy, stable healthy, stable unhealthy.
    """

    #Prepare the expected data as a Pandas Series
    expected_data = {'critical unhealthy':40, 'stable healthy':10, 'stable unhealthy':50}

    expected_series = pd.Series(data=expected_data,
                                index=['critical unhealthy', 'stable healthy', 'stable unhealthy'])

    # Run the  function to return the actual series
    actual_series = utils.get_existing_segments(df_input, 'status')

    # Compare actual vs expected
    assert_series_equal(actual_series,expected_series, check_names=False)


def test_get_existing_disease_segments():
    """
    This function will test that the expected series returned matches with the expected data that
     is diabetes, heart disease, hypertension and none
    """

    #Prepare the expected data as a Pandas Series
    expected_data = {'diabetes': 32, 'heart disease': 28,'hypertension': 16, 'none': 24}

    expected_series = pd.Series(data=expected_data,
                                index=['diabetes', 'heart disease','hypertension','none'])
    # Run the get_bmi_sgement function to return the actual series
    actual_series = utils.get_existing_segments(df_input, 'condition')

    # Compare actual vs expected
    assert_series_equal(actual_series,expected_series, check_names=False)


def test_get_postcode_segment():
    """
    This function will test that the expected series returned matches with
    the expected data that is Dublin 15 and Dublin 3.
    """
    #Prepare the expected data as a Pandas Series
    expected_data = {'Dublin 15': 1, 'Dublin 3': 1}

    expected_series = pd.Series(data=expected_data,
                                index=['Dublin 15', 'Dublin 3'])
    # Run the get_bmi_sgement function to return the actual series
    actual_series = utils.get_postcode_segment(df_input2)

    # Compare actual vs expected
    assert_series_equal(actual_series,expected_series, check_names=False)


def test_produce_health_stats():
    """
    This function will test that the expected series returned matches with the expected data that is
    index, timestamp, heart-rate, body temperature and blood sugar.
    :return:
    """

    # Create the expected outputs
    expected_index = [0, 1, 2, 3, 4]
    expected_timestamp = ['2021-08-05 16:18:00', '2021-08-05 19:53:00', '2021-08-04 23:38:00',
                          '2021-08-05 21:12:00', '2021-08-05 19:27:00']
    expected_heart_rate = [77, 70, 99, 130, 68]
    expected_body_temperature = [36.3, 35.39, 35.35, 35.08, 36.6]
    expected_blood_sugar = [329, 396, 396, 354, 389]

    #Call the function using Abigail Mercer as the person
    index, timestamp, heart_rate, body_temperature, blood_sugar = utils.produce_health_stats(df_input4, 'Abigail Mercer')

    assert index == expected_index
    assert timestamp == expected_timestamp
    assert heart_rate  == expected_heart_rate
    assert body_temperature == expected_body_temperature
    assert blood_sugar == expected_blood_sugar


def test_produce_blood_pressure():

    """
    This function will test that the expected series returned matches with the expected data that is index,
    timestamp, blood pressure top and blood pressure bottom.
    """
    # Create the expected outputs
    expected_index = [0, 1, 2, 3, 4]
    expected_timestamp = ['2021-08-05 16:18:00', '2021-08-05 19:53:00', '2021-08-04 23:38:00',
                          '2021-08-05 21:12:00', '2021-08-05 19:27:00']

    expected_blood_pressure_top = [131,104,204,123,114]
    expected_blood_pressure_bottom = [135,68,65,67,69]

    index, timestamp, blood_pressure_top, blood_pressure_bottom = utils.produce_blood_pressure(df_input4, 'Abigail Mercer')

    assert index == expected_index
    assert timestamp == expected_timestamp
    assert blood_pressure_top == expected_blood_pressure_top
    assert blood_pressure_bottom == expected_blood_pressure_bottom
