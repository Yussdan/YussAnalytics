"""
API Configuration Loader

This module loads and manages configuration settings for the API from environment variables. 
It uses the `dotenv` package to read variables from a `.env` file. The settings include 
API keys and credentials required for external services such as S3 storage.

Environment Variables:
    - api_key: The API key for accessing external services.
    - s3_key_id: The AWS S3 access key ID.
    - s3_key_pass: The AWS S3 secret access key.
    - bucket: The name of the S3 bucket to be used.

Usage:
    Simply import this module to access the loaded environment variables.
"""

import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("api_key")  # The API key for external services
s3_key_id = os.getenv("s3_key_id")  # S3 Access Key ID
s3_key_pass = os.getenv("s3_key_pass")  # S3 Secret Access Key
bucket = os.getenv("bucket")  # S3 Bucket name
