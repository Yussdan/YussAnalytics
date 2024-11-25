"""
Module to interact with S3 and manage file storage.

This module provides a class to connect to an S3-compatible service.
and perform file operations like uploading and downloading images.

Dependencies:
- boto3: AWS SDK for Python, used for interacting with S3-compatible services.
- logging: Used for logging error and important information messages.

Class:
- S3Client: A class that connects to S3, manages sessions, and handles file uploads and downloads.
"""
import logging
import boto3
import botocore.exceptions

logger = logging.getLogger('api')


class S3Client:
    """
    A class to interact with S3-compatible services.

    This class provides methods to connect to an S3 service and manage files, 
    including uploading and downloading files to/from S3.

    Attributes:
        aws_access_key_id (str): AWS access key ID.
        aws_secret_access_key (str): AWS secret access key.
        endpoint_url (str): The endpoint URL for S3 storage.
        region (str): The region for the S3 service (optional, default is "ru-central-1").

    Methods:
        _get_session: Creates an S3 session if it doesn't exist.
        _ensure_session: Ensures an active session is available.
        upload_image: Uploads an image file to an S3 bucket.
        download_image: Downloads an image file from an S3 bucket.
    """
    def __init__(self,
                aws_access_key_id=None,
                aws_secret_access_key=None,
                endpoint_url=None,
                region=None):
        """
        S3 client initialization.
        ::param aws_access_key_id: JAWS access key
        :param aws_secret_access_key: AWS secret key
        :param endpoint_url: S3 storage URL (optional).
        :param region: S3 region (optional).
        """
        self.aws_access_key_id =  aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.endpoint_url = endpoint_url or "https://s3.cloud.ru/"
        self.region = region or "ru-central-1"

        if not self.aws_access_key_id or not self.aws_secret_access_key:
            raise ValueError(
                "AWS keys must be specified either explicitly or through environment variables.")

        self.s3 = None

    def _get_session(self):
        """
        Creates an S3 session if it has not already been created.

        This method is responsible for setting up a session with the S3 service 
        using the provided AWS credentials, region, and endpoint URL.
        """
        if self.s3 is None:
            self.s3 = boto3.session.Session(
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                region_name=self.region
            ).client(service_name='s3', endpoint_url=self.endpoint_url)

    def _ensure_session(self):
        """
        Ensures an active session with S3 exists, creating it if necessary.

        This method checks whether an active S3 session exists. If not, it calls
        _get_session() to create a new session.
        """
        if not self.s3:
            self._get_session()

    def check_exist(self, bucket, bucket_file):
        """
        Check exist file
        """
        try:
            self.s3.head_object(Bucket=bucket, Key=bucket_file)
            return True
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                return False
            else:
                raise

    def upload_image(self, bucket: str, local_file: str, bucket_file: str):
        """
        Uploads an image file to an S3 bucket.

        This method uploads a local image file to a specified S3 bucket, saving 
        it under the given file name.

        Args:
            bucket (str): The name of the S3 bucket to upload to.
            local_file (str): The local file path to the image being uploaded.
            bucket_file (str): The destination file name in the S3 bucket.

        Returns:
            str: A success message indicating that the file was uploaded successfully.
        """
        self._ensure_session()
        self.s3.upload_fileobj(local_file, bucket, bucket_file)
        return f"File {local_file} successfully uploaded to {bucket}/{bucket_file}."

    def download_image(self, bucket: str, bucket_file: str):
        """
        Downloads an image file from an S3 bucket.

        This method retrieves a file from a specified S3 bucket and returns its contents.

        Args:
            bucket (str): The name of the S3 bucket to download from.
            bucket_file (str): The file name in the S3 bucket to download.

        Returns:
            bytes: The file content as bytes.

        Raises:
            Exception: If the file cannot be found or there is an issue with the download.
        """
        self._ensure_session()
        return self.s3.get_object(Bucket=bucket, Key=bucket_file)['Body'].read()
