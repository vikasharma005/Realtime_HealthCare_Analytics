import pandas as pd
from utils import functions as utils
from utils import config as config
import numpy as np

diseases = config.diseases
statuses = config.statuses
genders = config.genders
mock_ages_1 = config.mock_data["ages_low"]
mock_ages_2 = config.mock_data["ages_high"]
mock_bmi_1 = config.mock_data["bmi_low"]
mock_bmi_2 = config.mock_data["bmi_high"]
mock_temp_1 = config.mock_data["temp_low"]
mock_temp_2 = config.mock_data["temp_high"]
mock_heartrate_1 = config.mock_data["heartrate_low"]
mock_heartrate_2 = config.mock_data["heartrate_high"]
mock_bloodsugar_1 = config.mock_data["bloodsugar_low"]
mock_bloodsugar_2 = config.mock_data["bloodsugar_high"]
mock_systolic_1 = config.mock_data["systolic_low"]
mock_systolic_2 = config.mock_data["systolic_high"]
mock_diastolic_1 = config.mock_data["diastolic_low"]
mock_diastolic_2 = config.mock_data["diastolic_high"]


#df = pd.read_csv("./full_data.csv", low_memory=False)
#df = df.iloc[:3000]
#df = df[df['alert'].notna()]
#df = df.sort_values('reading_id', ascending=False)

#df.to_csv("test_data2.csv")
#input_df_2 = pd.read_csv("../test_data/test_data2.csv")

#df = utils.create_alert_table(input_df_2)
#df.to_csv("result_data2.csv", index=False)
#patients, readings, alerts, emergencies, warnings = utils.get_total_counts(input_df_2)
#print (patients, readings, alerts, emergencies, warnings )

df = pd.read_csv("./test_data/test_data4.csv")



index, timestamp, heart_rate, body_temperature, blood_sugar = utils.produce_health_stats(df,'Abigail Mercer')
print(index)
print(timestamp)
print(heart_rate)
print(body_temperature)
print(blood_sugar)


#df = utils.filter_dataframe(df_input1, diseases, statuses, mock_ages_2, genders,mock_bmi_1, mock_temp_1, mock_heartrate_1, mock_bloodsugar_1,mock_systolic_1, mock_diastolic_1)

#print(df)

#df.to_csv("result_data3.csv", index=False)

