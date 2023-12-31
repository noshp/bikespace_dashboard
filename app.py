import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import requests

st.title("Bikespace Dashboard")

# https://api-dev.bikespace.ca/api/v2/docs 
def get_submission_data():
    url = 'https://api-dev.bikespace.ca/api/v2/submissions'
    headers = {'accept': 'application/json'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        # Handle the error, raise an exception, or return an empty list, depending on your use case.
        return []

def submissions_to_dataframe(submissions):
    data = []
    for submission in submissions:
        row = {
            'id': submission['id'],
            'comments': submission['comments'],
            'issues': ', '.join(submission['issues']),
            'latitude': submission['latitude'],
            'longitude': submission['longitude'],
            'parking_duration': submission['parking_duration'],
            'parking_time': pd.to_datetime(submission['parking_time'])
        }
        data.append(row)
    return pd.DataFrame(data)

# Fetch data and convert to DataFrame
submissions_data = get_submission_data()
chart_data = submissions_to_dataframe(submissions_data)


st.pydeck_chart(pdk.Deck(
    map_style=None,
    initial_view_state=pdk.ViewState(
        latitude=43.651070,
        longitude=-79.347015,
        zoom=11,
        pitch=40.5,
        bearing=-27.36,
    ),
    layers=[
        pdk.Layer(
            'HexagonLayer',
            data=chart_data,
            get_position='[longitude, latitude]',
            get_color='[200, 30, 0, 160]',
            get_radius=200,
            auto_highlight=True,
            elevation_scale=50,
            pickable=True,
            elevation_range=[0, 3000],
            extruded=True,
            coverage=1,
        ),
    ],
))