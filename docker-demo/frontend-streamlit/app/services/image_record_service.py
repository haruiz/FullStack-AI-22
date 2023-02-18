import os
from pathlib import Path
import requests


class ImageRecordService:
    def __init__(self):
        self._api_endpoint = f"{os.environ['API_ENDPOINT']}/images"

    def add_image(self, bytes_data, image_file: Path, label_id):
        """
        Add an image to the database
        :param image_file: the image file
        :param label: the label of the image
        :return:
        """
        payload = {"label": label_id}
        files = {"image": (image_file, bytes_data, "image/jpeg")}
        response = requests.request(
            "POST", self._api_endpoint, headers={}, data=payload, files=files
        )
        return response
