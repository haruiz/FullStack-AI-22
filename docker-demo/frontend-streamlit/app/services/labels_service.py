import json
import os

import requests


class LabelsService:
    def __init__(self):
        self._api_endpoint = f"{os.environ['API_ENDPOINT']}/labels"

    def add_label(self, label_text):
        """
        Add a label to the database
        :param label_text:
        :return:
        """

        payload = json.dumps({"label": label_text})
        headers = {"Content-Type": "application/json"}
        url = self._api_endpoint
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.json()

    def fetch_labels(self):
        """
        Fetch all labels from the database
        :return:
        """

        url = self._api_endpoint
        response = requests.request("GET", url)
        return response.json()
