import os
from google.cloud import storage


class GCPUtils:
    @staticmethod
    def get_gcp_project_id() -> str:
        """
        Get the GCP project ID
        :return:
        """
        return os.environ.get("GCP_PROJECT_ID", "")

    @staticmethod
    def get_list_of_buckets() -> list[str]:
        """
        Get a list of buckets
        :return:
        """
        storage_client = storage.Client()
        buckets = storage_client.list_buckets()
        return [bucket.name for bucket in buckets]

    @staticmethod
    def upload_file_to_bucket(
        bucket_name: str, file_bytes: bytes, destination_blob_name: str
    ):
        """
        Upload a file to a GCP bucket
        :param bucket_name:
        :param file_bytes:
        :param destination_blob_name:
        :return:
        """
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob: storage.Blob = bucket.blob(destination_blob_name)
        blob.upload_from_string(file_bytes, content_type="image/jpeg")
        url = blob.public_url
        return url
