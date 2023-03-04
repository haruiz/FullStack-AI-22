import streamlit as st
import pandas as pd
import numpy as np


st.set_page_config(
    page_title="Dashboard",
    layout="wide"
)


def load_data():
    dataset_uri = "https://gist.githubusercontent.com/curran/a08a1080b88344b0c8a7/raw/0e7a9b0a5d22642a06d3d5b9bcbad9890c8ee534/iris.csv"
    df = pd.read_csv(dataset_uri)
    return df


st.title("Hello world from streamlit!")
i_was_clicked = st.button("click me!!")

if i_was_clicked:
    st.write("Hey!!, you did it!")

data = load_data()

# render a visual widget
st.table(data.head(10))

# # plot the histogram
# sepal_length_data = data["sepal_length"]
# st.bar_chart(sepal_length_data)

columns = data.columns
option = st.selectbox(
    'What variable would you like to plot?',
    columns)

st.write('You selected:', option)


st.bar_chart(data[option])


 


