# Import required libraries

import copy
import pathlib

import dash
import pandas as pd
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go


# Import Utility functions from the util directory/package
from utils import functions as util
from utils import config as config
import pathlib
# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()

app = dash.Dash(__name__,
                meta_tags=[{"name": "viewport", "content": "width=device-width"}], )

app.title = "RTHCA: Realtime Healthcare Analytics "
server = app.server

# --------- LOAD DATA --------- #
"""
Use cassandra to load the data
"""
source = "cassandra"

if source == 'cassandra':
    df = util.read_cassandra(config.host, config.username, config.password, config.keyspace)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
else:
    df = pd.read_csv("test_data/full_data.csv", low_memory=False)
    df["timestamp"] = pd.to_datetime(df["timestamp"])

# Calculate the counts
total_patients, total_readings, total_alerts, total_emergencies, total_warnings = util.get_total_counts(df)
hypertension, hypothermia, hyperthermia, fever, hyperglycemia, tachycardia = util.get_alert_counts(df)

# --------- DASH LAYOUT --------- #
layout = dict(autosize=True, automargin=True, margin=dict(l=30, r=30, b=20, t=40), hovermode="closest",
              plot_bgcolor="#F9F9F9", paper_bgcolor="#F9F9F9", title="Location of Sensor Readings",
              legend=dict(font=dict(size=10), orientation="h"),marker = {'size': 12},
              mapbox=dict(accesstoken=config.mapbox_access_token, style="light", center=dict(lon=-6.317, lat=53.335), zoom=11),
              )

# Create app layout
app.layout = html.Div(
    [
        dcc.Store(id="aggregate_data"),
        # empty Div to trigger javascript file for graph resizing
        html.Div(id="output-clientside"),
        html.Div(
            [
                html.Div(
                    [
                        html.Img(
                            src=app.get_asset_url("dash.png"),
                            id="plotly-image",
                            style={
                                "height": "auto",
                                "width": "auto",
                                "padding": "5px",
                                "margin-top": "0px",
                                "margin-bottom": "0px",
                            },
                        )
                    ],
                    className="one-third column",
                ),
                html.Div(
                    [
                        html.Div(
                           
                        )
                    ],
                    className="one-half column",
                    id="title",
                ),
                html.Div(
                    [
			html.Img(
                            src=app.get_asset_url("email.png"),
                            id="email-image",
                            style={
                                "height": "auto",
                                "width": "auto",
                                "margin-top": "0px",
                                "margin-bottom": "0px",
                                "float": "right",
                                "padding": "5px",
                                "title":"My Github",
                            },
                        ),
                        html.Img(
                            src=app.get_asset_url("linkedin.png"),
                            id="linkedin-image",
                            style={
                                "height": "auto",
                                "width": "auto",
                                "margin-top": "0px",
                                "float": "right",
                                "padding": "5px",
                                "margin-bottom": "0px",
                                "title":"My Github",
                            },
                        ),
                        html.Img(
                            src=app.get_asset_url("github.png"),
                            id="github-image",
                            style={
                                "height": "auto",
                                "width": "auto",
                                "float": "right",
                                "padding": "5px",
                                "margin-top": "0px",
                                "margin-bottom": "0px",
                                "title":"My Github",
                            },
                        )
                    ],
                    
                    className="one-third column",
                    id="button",
                ),
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "0px", 'font-color': 'white'},
        ),
        html.Div(
            [
                html.Div(
                    [   html.Strong("Patient Filters"),
                        html.P("Filter by Diseases:", className="control_label"),
                        dcc.RadioItems(
                            id="disease_selector",
                            options=[
                                {"label": "All ", "value": "all"},
                                {"label": "None", "value": "none"},
                                {"label": "Custom ", "value": "custom"},
                            ],
                            value="none",
                            labelStyle={"display": "inline-block"},
                            className="dcc_control",
                        ),
                        dcc.Dropdown(
                            id="diseases",
                            options=config.disease_options,
                            multi=True,
                            value=config.diseases,
                            className="dcc_control",
                        ),
                        dcc.Checklist(
                            id="lock_selector",
                            options=[{"label": "Lock camera", "value": "locked"}],
                            className="dcc_control",
                            value=[],
                        ),
                        html.P("Filter by Health Statuses:", className="control_label"),
                        dcc.RadioItems(
                            id="health_status_selector",
                            options=[
                                {"label": "All ", "value": "all"},
                                {"label": "Stable", "value": "stable"},
                                {"label": "Customize ", "value": "custom"},
                            ],
                            value="stable",
                            labelStyle={"display": "inline-block"},
                            className="dcc_control",
                        ),
                        dcc.Dropdown(
                            id="health_statuses",
                            options=config.health_options,
                            multi=True,
                            value=config.statuses,
                            className="dcc_control",
                        ),
                        html.P("Filter by Gender:", className="control_label"),
                        dcc.RadioItems(
                            id="gender_selector",
                            options=[
                                {"label": "Both ", "value": "Both"},
                                {"label": "Male", "value": "Male"},
                                {"label": "Female ", "value": "Female"},
                            ],
                            value="Both",
                            labelStyle={"display": "inline-block"},
                            className="dcc_control",
                        ),
                        dcc.Dropdown(
                            id="genders",
                            options=config.gender_options,
                            multi=True,
                            value=config.genders,
                            className="dcc_control",
                        ),
                        html.P(
                            "Select Age Range:",
                            className="control_label",
                        ),
                        dcc.RangeSlider(
                            id="age_slider",
                            min=18,
                            max=95,
                            value=[18, 95],
                            marks={18: "18",
                                   30: "30",
                                   40: "40",
                                   50: "50",
                                   60: "60",
                                   70: "70",
                                   80: "80",
                                   90: "90",
                                   100: "100"},

                            className="dcc_control",
                        ),
                        html.P(
                            "Select BMI Range:",
                            className="control_label",
                        ),
                        dcc.RangeSlider(
                            id="bmi_slider",
                            min=18,
                            max=45,
                            value=[25, 30],
                            marks={18: "18",
                                   25: "25",
                                   30: "30",
                                   35: "35",
                                   40: "40"
                                   },

                            className="dcc_control",
                        ),
                        html.Br(),
                        html.Strong("Sensor Reading Filters"),
                        html.P(
                            "Select Heart Rate Range:",
                            className="control_label",
                        ),
                        dcc.RangeSlider(
                            id="heart_rate_slider",
                            min=40,
                            max=300,
                            value=[60, 120],
                            marks={40: "40",
                                   60: "60",
                                   80: "80",
                                   120: "120",
                                   160: "160",
                                   200: "200"
                                   },

                            className="dcc_control",
                        ),
                        html.P(
                            "Select Body Temperature Range:",
                            className="control_label",
                        ),
                        dcc.RangeSlider(
                            id="body_temperature_slider",
                            min=33,
                            max=42,
                            value=[35, 38],
                            marks={33: "33.0",
                                   35: "35.0",
                                   37: "37.0",
                                   39: "39.0",
                                   41: "41.0",
                                   },

                            className="dcc_control",
                        ),
                        html.P(
                            "Select Blood Sugar Range:",
                            className="control_label",
                        ),
                        dcc.RangeSlider(
                            id="blood_sugar_slider",
                            min=35,
                            max=500,
                            value=[50, 250],
                            marks={35: "35",
                                   150: "150",
                                   250: "250",
                                   350: "350",
                                   500: "500",
                                   },
                            className="dcc_control",
                        ),
                        html.P(
                            "Select Systolic BP Range:",
                            className="control_label",
                        ),
                        dcc.RangeSlider(
                            id="systolic_slider",
                            min=100,
                            max=220,
                            value=[100, 160],
                            marks={100: "100",
                                   120: "120",
                                   140: "140",
                                   160: "160",
                                   180: "180",
                                   200: "200",
                                   220: "220"
                                   },

                            className="dcc_control",
                        ),
                        html.P(
                            "Select Diastolic BP Range:",
                            className="control_label",
                        ),
                        dcc.RangeSlider(
                            id="diastolic_slider",
                            min=50,
                            max=150,
                            value = [80,120],
                            marks={50: "50",
                                   75: "75",
                                   100: "100",
                                   125: "125",
                                   150: "150"
                                   },

                            className="dcc_control",
                        ),
                    ],
                    className="pretty_container four columns",
                    id="cross-filter-options",
                ),
                html.Div(
                    [html.P("Overview of Healthcare Data", className="control_label"),
                        html.Div(
                            [
                                html.Div(
                                    [ html.Strong(str(total_patients), style={'font-size': '40px'})
                                    ,html.H6(id="numberPatients"),
                                    html.P("Total Patients"),
                                    ],
                                    id="patients",
                                    className="mini_container",
                                    style={'background': config.gradient_green}
                                ),
                                html.Div(
                                    [html.Strong(str(total_readings), style={'font-size': '40px'}),
                                    html.H6(id="numberReadings"),
                                     html.P("Sensor Readings Recorded")
                                     ],
                                    id="readings",
                                    className="mini_container",
                                    style={'background': config.gradient_green}
                                ),
                                html.Div(
                                    [html.Strong(str(total_alerts), style={'font-size': '40px'}),
                                    html.H6(id="numberAlerts"),html.P("Total Alerts Detected")
                                    ],
                                    className="mini_container",
                                    style={'background': config.gradient_green}
                                ),
                                html.Div(
                                    [html.Strong(str(total_emergencies),style={'font-size': '40px'}),
                                    html.H6(id="numberEmergencies"), 
                                    html.P("Total Emergencies Reported")
                                     ],
                                    id="emergencies",
                                    className="mini_container",
                                    style={'background': config.gradient_green}
                                ),
                                html.Div(
                                    [html.Strong(str(total_warnings),style={'font-size': '40px'}),
                                    html.H6(id="numberWarnings"), 
                                    html.P("Total Warnings Reported")
                                     ],
                                    id="warnings",
                                    className="mini_container",
                                    style={'background': config.gradient_green}
                                ),
                            
                            ],
                            id="info-container",
                            style={'color': '#FFFFFF', 'opacity': 0.9, 'align': 'center'},
                            className="row container-display",
                        ),html.P("Breakdown of Detected Alerts", className="control_label"),
                            html.Div(
                            [
                                html.Div(
                                    [
                                        html.Strong(str(hypertension), style={'font-size': '25px'}),
                                        html.H6(id="numHypertension"),
                                        html.P("Hypertension",style={'font-size': '16px'}),
                                    ],
                                    id="hypertension",
                                    style={'background': config.gradient_red,
                                           'color': '#FFFFF'},
                                    className="mini_container",
                                ),
                                html.Div(
                                    [
                                        html.Strong(str(hypothermia), style={'font-size': '25px'}),
                                        html.H6(id="numHypothermia"),
                                        html.P("Hypothermia",style={'font-size': '16px'}),
                                    ],
                                    id="hypothermia",
                                    style={'background': config.gradient_red,
                                           'color': '#FFFFF'},
                                    className="mini_container",
                                ),
                                html.Div(
                                    [
                                        html.Strong(str(hyperthermia), style={'font-size': '25px'}),
                                        html.H6(id="numHyperthermia"),
                                        html.P("Hyperthermia",style={'font-size': '16px'}),
                                    ],
                                    id="hyperthermia",
                                    style={'background': config.gradient_red,
                                           'color': '#FFFFF'},
                                    className="mini_container",
                                ),
                                html.Div(
                                    [
                                        html.Strong(str(hyperglycemia), style={'font-size': '25px'}),
                                        html.H6(id="numHyperglycemia"),
                                        html.P("Hyperglycemia",style={'font-size': '16px'}),
                                    ],
                                    id="hyperglycemia",
                                    style={
                                        'background': config.gradient_red,
                                        'color': '#FFFFF'},
                                    className="mini_container",
                                ),
                                html.Div(
                                    [
                                        html.Strong(str(fever), style={'font-size': '25px'}),
                                        html.H6(id="numFever"),
                                        html.P("Fever/Pyrexia",style={'font-size': '16px'}),
                                    ],
                                    id="fever",
                                    style={
                                           'background': config.gradient_yellow,
                                           'color': '#FFFFF'},
                                    className="mini_container",
                                ),
                                html.Div(
                                    [
                                        html.Strong(str(tachycardia), style={'font-size': '25px'}),
                                        html.H6(id="numTachycardia"),
                                        html.P("Tachycardia",style={'font-size': '16px'}),
                                     ],
                                    id="tachycardia",
                                    style={
                                           'background': config.gradient_yellow,
                                           'color': '#FFFFF'},
                                    className="mini_container",
                                ),
                            ],
                            id="info-container2",
                            style={'color': '#FFFFFF', 'opacity': 0.9},
                            className="row container-display",
                        ),
                     html.Br(),
                        html.P("Detected Patient Alerts", className="control_label"),
                     html.Br(),

                        html.Div(util.create_alert_graph(df),style={'margin-top': '10px'}
                        ),
                    

                    ],
                    id="right-column",
                    className="eight columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [ html.P("Patient Sensor Readings"),
                        dcc.Graph(id="main_graph")],
                    className="pretty_container seven columns",
                ),
                html.Div(
                    [ html.P("Patient's Main Health Stats"),
                        dcc.Graph(id="health_graph")],
                    className="pretty_container five columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [html.P("All Patient Statistics:"),
                     dcc.Dropdown(
                         id='names',
                         value='Patients by BMI',
                         options=[{'value': x, 'label': x}
                                  for x in config.patient_statistics],
                         clearable=False,
                     ),
                     dcc.Graph(id="pie-chart"),
                     ],
                    className="pretty_container seven columns",
                ),
                html.Div(
                    [ html.P("Patient's Blood Pressure Stats"),
                      dcc.Graph(id="blood_pressure_graph")],
                    className="pretty_container five columns",
                ),
            ],
            className="row flex-display",
        ),
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)


# ---- Display the filters on left menu ---- #

# Radio -> multi
@app.callback(
    Output("diseases", "value"), [Input("disease_selector", "value")]
)
def display_condition(selector):
    if selector == "all":
        return config.diseases
    elif selector == "none":
        return ["none"]
    return []


# Radio -> multi
@app.callback(Output("health_statuses", "value"), [Input("health_status_selector", "value")])
def display_health(selector):
    if selector == "all":
        return config.statuses
    elif selector == "stable":
        return ["stable unhealthy", "stable healthy"]
    return []

# Radio -> multi
@app.callback(
    Output("genders", "value"), [Input("gender_selector", "value")]
)
def display_gender(selector):
    if selector == "Both":
        return config.genders
    elif selector == "Male":
        return ["Male"]
    elif selector == "Female":
        return ["Female"]
    return []


@app.callback(
    Output("main_graph", "figure"),
    [
        Input("diseases", "value"), Input("health_statuses", "value"), Input("age_slider", "value"),
        Input("genders", "value"), Input("bmi_slider", "value"), Input("body_temperature_slider", "value"),
        Input("heart_rate_slider", "value"), Input("blood_sugar_slider", "value"),
        Input("systolic_slider", "value"), Input("diastolic_slider", "value"),
    ],
    [State("lock_selector", "value"), State("main_graph", "relayoutData")],
)
def make_main_figure(disease, statuses, age_slider, gender,bmi_slider, temperature_slider,
                     heartrate_slider, bloodsugar_slider, systolic_slider, diastolic_slider,
                     selector, main_graph_layout):

    #Filter the dataframe by passing in dataframe and the variables from the filters
    filtered_data = util.filter_dataframe(df, disease, statuses, age_slider, gender,
                                           bmi_slider, temperature_slider, heartrate_slider,
                                           bloodsugar_slider, systolic_slider, diastolic_slider)
    names = filtered_data['name'].unique()
    #filtered_data = filtered_data.to_dict("records")
    traces = []
    for name in names:
        new_df = filtered_data[filtered_data["name"]==name]
        trace = dict( type="scattermapbox",
                      hover_name=new_df["name"],
                      lon=new_df["longitude"],
                      lat=new_df["latitude"],
                      text=new_df["timestamp"],
                      customdata=new_df["name"],
                      legend=new_df["name"],
                      name = name,
                      marker=dict(size=4, opacity=0.6),
            )
        traces.append(trace)

    # relayoutData is None by default, and {'autosize': True} without relayout action
    if main_graph_layout is not None and selector is not None and "locked" in selector:
        if "mapbox.center" in main_graph_layout.keys():
            lon = float(main_graph_layout["mapbox.center"]["lon"])
            lat = float(main_graph_layout["mapbox.center"]["lat"])
            zoom = float(main_graph_layout["mapbox.zoom"])
            layout["mapbox"]["center"]["lon"] = lon
            layout["mapbox"]["center"]["lat"] = lat
            layout["mapbox"]["zoom"] = zoom

    figure = dict(data=traces, layout=layout)
    return figure




# Main graph -> individual graph
@app.callback(Output("health_graph", "figure"),
              [Input("main_graph", "hoverData")])
def make_person_health_figure(main_graph_hover):

    layout_individual = copy.deepcopy(layout)

    if main_graph_hover is None:
        main_graph_hover = {
            'points': [
                {'curveNumber': 0, 'pointNumber': 0, 'customdata': 'Non-Selected'}
            ]
        }

    print(main_graph_hover)

    # Every time we mouse over the map it creates a list called points. We select the person's name
    name = [person["customdata"] for person in main_graph_hover["points"]]
    index, timestamp, heart_rate, body_temperature, blood_sugar = util.produce_health_stats(df,name[0])

    if index is None:
        annotation = dict(
            text="No data available",
            x=timestamp,
            y=0.5,
            align="center",
            showarrow=False,
            xref="paper",
            yref="paper",
        )
        layout_individual["annotations"] = [annotation]
        data = []
    else:
        data = [
            dict(
                type="scatter",
                mode="lines+markers",
                name="Heart Rate (bpm)",
                x=timestamp,
                y=heart_rate,
                line=dict(shape="spline", smoothing=2, width=1, color="#5bbafa"),
                marker=dict(symbol="circle")
            ),
            dict(
                type="scatter",
                mode="lines+markers",
                name="Body Temperature (Celsius)",
                x=timestamp,
                y=body_temperature,
                line=dict(shape="spline", smoothing=2, width=1, color="#ffcf93"),
                marker=dict(symbol="circle"),
            ),
            dict(
                type="scatter",
                mode="lines+markers",
                name="Blood Sugar mg/DL",
                x=timestamp,
                y=blood_sugar,
                line=dict(shape="spline", smoothing=2, width=1, color="#f8a5af"),
                marker=dict(symbol="circle")
            ),
        ]
        layout_individual["title"] = name[0]

    figure = dict(data=data, layout=layout_individual)
    return figure


# Main graph -> individual graph
@app.callback(Output("blood_pressure_graph", "figure"),
              [Input("main_graph", "hoverData")])
def make_blood_pressure_figure(main_graph_hover):

    layout_individual = copy.deepcopy(layout)

    if main_graph_hover is None:
        main_graph_hover = {
            'points': [
                {'curveNumber': 0, 'pointNumber': 0, 'customdata': 'Non-Selected'}
            ]
        }

    # Every time we mouse over the map it creates a list called points. We select the person's name
    name = [person["customdata"] for person in main_graph_hover["points"]]
    index, timestamp,blood_pressure_top, blood_pressure_bottom = util.produce_blood_pressure(df,name[0])

    if index is None:
        annotation = dict(
            text="No data available",
            x=timestamp,
            y=0.5,
            align="center",
            showarrow=False,
            xref="paper",
            yref="paper",
        )
        layout_individual["annotations"] = [annotation]
        data = []
    else:
        data = [
            dict(
                type="scatter",
                mode="lines+markers",
                name="Systolic Blood Pressure",
                x=timestamp,
                y=blood_pressure_top,
                line=dict(shape="spline", smoothing=2, width=1, color="#a48afa"),
                marker=dict(symbol="circle"),
            ),

            dict(
                type="lines+markers",
                mode="lines+markers",
                name="Diastolic Blood Pressure",
                x=timestamp,
                y=blood_pressure_bottom,
                line=dict(shape="spline", smoothing=2, width=1, color="#dfb0ff"),
                marker=dict(symbol="circle"),
            ),
        ]

        layout_individual["title"] = name[0]

    figure = dict(data=data, layout=layout_individual)
    return figure


@app.callback(
    Output("pie-chart", "figure"),
    [Input("names", "value")])
def generate_segment_charts(names):

    if names == 'Patients by BMI':
        segment = util.get_bmi_segment(df)
        fig = go.Figure(data=[go.Pie(labels=segment.index.values, values=segment.values, name="BMI",
                                     hole=.4, hoverinfo="label+percent+name+value",
                                     marker=dict(colors=config.color_map_small, line=dict(color='#f9f9f9', width=1)))])

    if names == 'Patients by Health Status':
        segment = util.get_existing_segments(df, 'status')
        fig = go.Figure(data=[go.Pie(labels=segment.index.values, values=segment.values, name="Health",
                                     hole=.6, hoverinfo="label+percent+name+value",
                                     marker=dict(colors=config.color_map_small, line=dict(color='#f9f9f9', width=1)))])

    if names == 'Patients by Age':
        segment = util.get_age_segment(df)
        fig = go.Figure(data=[go.Pie(labels=segment.index.values, values=segment.values, name="Age",
                                     hoverinfo="label+percent+name+value",
                                     marker=dict(colors=config.color_map_small, line=dict(color='#f9f9f9', width=1)))])

    if names == 'Patients by Condition':
        segment = util.get_existing_segments(df, 'condition')
        fig = go.Figure(data=[go.Pie(labels=segment.index.values, values=segment.values, name="Condition",
                                     hoverinfo="label+percent+name+value",
                                     marker=dict(colors=config.color_map_small, line=dict(color='#f9f9f9', width=1)))])

    if names == 'Patients by Gender':
        segment = util.get_existing_segments(df,'gender')
        fig = go.Figure(data=[go.Pie(labels=segment.index.values, values=segment.values, name="Gender",
                                     hole=.25, hoverinfo="label+percent+name+value",
                                     marker=dict(colors=config.color_map_small, line=dict(color='#f9f9f9', width=1)))])

    if names == 'Patients by Postcode':
        segment = util.get_postcode_segment(df)
        fig = go.Figure(data=[go.Bar(x=segment.index.values, y=segment.values, name="Postcode",
                                     marker_color=config.color_map_full)])

    fig.update_layout(plot_bgcolor='rgb(255,255,255)')
    return fig


# Main
if __name__ == "__main__":
    app.run_server(debug=True)
    #app.run_server(debug=False,dev_tools_ui=False,dev_tools_props_check=False)


