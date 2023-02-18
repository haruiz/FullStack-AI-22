import streamlit as st
from PIL import Image
from app.services import LabelsService, ImageRecordService
from decouple import config
import os

# set the api endpoint
if "API_ENDPOINT" not in os.environ:
    os.environ["API_ENDPOINT"] = config("API_ENDPOINT")

labels_service = LabelsService()
image_record_service = ImageRecordService()

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://www.extremelycoolapp.com/help",
        "Report a bug": "https://www.extremelycoolapp.com/bug",
        "About": "# This is a header. This is an *extremely* cool app!",
    },
)

st.write("# Image Annotation Tool! 👋")
st.text("This app is used to annotate images")

# get all the labels from the database through the labels service and populate the radio button
labels_dict = labels_service.fetch_labels()
labels_dict = {label["label"]: label["label_id"] for label in labels_dict}

if len(labels_dict) == 0:
    st.warning("No labels found! Please add a label first.")
    st.stop()

tab1, tab2 = st.tabs(["Load Image", "Take a picture"])

with tab1:
    # render the file uploader widget
    uploaded_file = st.file_uploader(
        "1.Choose a file to annotate", type=["png", "jpg", "jpeg"]
    )
    # if the user uploaded an image, display it
    if uploaded_file is not None:
        image_bytes_data = uploaded_file.getvalue()
        file_name = uploaded_file.name
        image = Image.open(uploaded_file)
        st.image(image, caption=uploaded_file.name, use_column_width=True)

with tab2:
    # render the camera input widget
    picture = st.camera_input("Take a picture")
    if picture:
        image_bytes_data = picture.getvalue()  # get the bytes data from the image
        file_name = "picture.jpg"

# add a radio button to select the label
label = st.radio("2.Assign a label to the image", labels_dict)

if label:
    st.write(f"Label assigned: {label}")

# add a button to annotate the image
button = st.button("Annotate")
if button and image_bytes_data:
    # get the bytes data from the uploaded file
    response = image_record_service.add_image(
        image_bytes_data, file_name, labels_dict[label]
    )
    is_success = response.status_code == 200
    if is_success:
        st.success("Image annotated!", icon="✅")  # display a success message
        st.balloons()
    else:
        st.error("Something went wrong!", icon="❌")  # display an error message
        st.write(response.json()["detail"])
