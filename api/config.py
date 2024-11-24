import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("api_key")
s3_key_id = os.getenv('s3_key_id')
s3_key_pass = os.getenv('s3_key_pass')
bucket = os.getenv('bucket')