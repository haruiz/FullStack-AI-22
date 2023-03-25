import streamlit as st
from decouple import config
import os
import requests
import json

# set the api endpoint in development mode
if "API_ENDPOINT" not in os.environ:
    os.environ["API_ENDPOINT"] = config("API_ENDPOINT")


def call_api(sepal_length, sepal_width, petal_length, petal_width):
    # call the api
    payload = json.dumps([{
            "sepal_length": sepal_length,
            "sepal_width": sepal_width,
            "petal_length": petal_length,
            "petal_width": petal_width
    }])
    headers = {
        'Content-Type': 'application/json'
    }

    url = os.environ["API_ENDPOINT"] + "/iris/predict"
    response = requests.request("POST", url, headers=headers, data=payload)
    results = response.json()
    return results


st.set_page_config(
    page_title="Iris App",
    layout="wide"
)

st.title("Hello world from streamlit!")

st.write("This is a demo app for the course: Fullstack AI projects")

sepal_length = st.number_input('Insert a sepal length', value=5.1)
sepal_width = st.number_input('Insert a sepal width', value=3.5)
petal_length = st.number_input('Insert a petal length', value=1.4)
petal_width = st.number_input('Insert a petal width', value=0.2)

i_was_clicked = st.button("Run Inference")
if i_was_clicked:
    # call the api
    results = call_api(sepal_length, sepal_width, petal_length, petal_width)
    st.write(results)
    st.balloons()
