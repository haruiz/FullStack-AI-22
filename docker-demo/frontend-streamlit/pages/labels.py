import pandas as pd
import streamlit as st
from app.services import LabelsService

labels_service = LabelsService()


def render_labels_table():
    """
    Populate the labels table
    :return:
    """
    labels = labels_service.fetch_labels()
    df = pd.DataFrame(labels)
    if not df.empty:
        df = df[["label", "description"]]
    st.table(df)


def render_new_label_form():
    """
    Create a form to add a label
    :return:
    """
    label_text = st.text_input("Label")
    if st.button("Add label") and label_text:
        labels_service.add_label(label_text)


st.set_page_config(
    page_title="Labels page",
    page_icon="👋",
)

st.header("Labels page")

render_new_label_form()  # render the form to add a new label
render_labels_table()  # render the table with all the labels
