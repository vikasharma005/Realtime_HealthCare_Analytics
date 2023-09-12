"""
This file includes all the configuration required for Plotly Dash Dashboard

"""

# --------- CASSANDRA CONFIGURATION --------- #

host = '127.0.0.1'
username = 'cassandra'
password = 'cassandra'
keyspace = 'healthcare_db'
fetch_size = 10000000

# --------- DASH CONFIGURATION --------- #

# Dash configuration for dropdowns
diseases = ['diabetes', 'hypertension', 'heart disease', 'none']
genders = ["Male", "Female"]
statuses = ['stable unhealthy','stable healthy','critical unhealthy', 'emergency']


gender_options = [{'label': 'Female', 'value': 'Female'},
                   {'label': 'Male', 'value': 'Male'}]

disease_options = [{'label': 'diabetes', 'value': 'diabetes'},
                   {'label': 'hypertension', 'value': 'hypertension'},
                   {'label': 'heart disease', 'value': 'heart disease'},
                   {'label': 'none', 'value': 'none'}]

health_options = [{'label': 'stable unhealthy', 'value': 'stable unhealthy'},
                  {'label': 'stable healthy', 'value': 'stable healthy'},
                  {'label': 'critical unhealthy', 'value': 'critical unhealthy'},
                  {'label': 'emergency', 'value': 'emergency'}]

patient_statistics = ['Patients by BMI', 'Patients by Health Status', 'Patients by Age',
                      'Patients by Condition', 'Patients by Gender', 'Patients by Postcode']


# Create global chart template
mapbox_access_token = "pk.eyJ1IjoiYnJpYW5ob3VyaWdhbiIsImEiOiJja3JtN2VhOTUxbm5wMnBvNWVia2tncW92In0.tRvm3Wd57OOxTYGaDydSTw"


gradient_yellow = 'linear-gradient(90deg, rgba(52,52,52,0.8869748583026961) 0%, rgba(2,195,128,1) 0%, rgba(13,240,161,1) 100%)'
gradient_blue = 'linear-gradient(207deg, rgba(2,0,36,1) 0%, rgba(77,176,253,1) 0%, rgba(54,126,255,1) 100%)'
gradient_green = 'linear-gradient(90deg, rgba(52,52,52,0.8869748583026961) 0%, rgba(3,171,172,1) 0%, rgba(0,217,222,1) 100%'
gradient_red = 'linear-gradient(90deg, rgba(52,52,52,0.8869748583026961) 0%, rgba(191,21,88,1) 0%, rgba(240,65,127,1) 100%)'
gradient = 'linear-gradient(262deg, rgba(2,0,36,1) 0%, rgba(33,153,213,1) 0%, rgba(0,212,255,1) 100%)'


# Color Maps to change the colors oh the all patient Statisc
color_map_bmi = ['#242038', '#725AC1', '#8D86C9', '#CAC4CE', '#F7ECE1']
color_map_health = ['#2e1e3b', '#413d7b', '#37659e', '#348fa7', '#40b7ad', '#8bdab2']
color_map_age = ['#26818e', '#228b8d', '#1f958b', '#1fa088', '#24aa83', ]
color_map_condition = ['#2fb47c', '#42be71', '#58c765', '#70cf57', '#8bd646']
color_map_gender = ['#a8db34', '#c5e021', '#e2e418', '#fde725']

color_map_full = ['#440154', '#471164', '#482071', '#472e7c', '#443b84',
                  '#2e1e3b', '#413d7b', '#37659e', '#348fa7', '#40b7ad', '#8bdab2',
                  '#26818e', '#228b8d', '#1f958b', '#1fa088', '#24aa83',
                  '#2fb47c', '#42be71', '#58c765', '#70cf57', '#8bd646',
                  '#a8db34', '#c5e021', '#e2e418', '#fde725']

color_map_small = ['#f2aebb', '#b6d8ef', '#f7e0a8', '#bead9e', '#b1a5c0','#f5c9d9', '#bead9e', '#f6c89f', '#f6c89f']



