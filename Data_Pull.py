import os
import boto3
import pandas as pd
import io


# Read in the CSV File from AWS
ACCESS_KEY_ID = os.environ['ACCESS_KEY_ID']
ACCESS_SECRET_KEY = os.environ['ACCESS_SECRET_KEY']
BUCKET_NAME = 'mypersonalprojects'
REGION_NAME = 'us-east-2'
FILE_NAME = "Jeapordy/game_data.csv"
s3_client = boto3.client(
        service_name='s3',
        aws_access_key_id=ACCESS_KEY_ID,
        aws_secret_access_key=ACCESS_SECRET_KEY,
        region_name=REGION_NAME
    )


def get_data():
    obj = s3_client.get_object(Bucket=BUCKET_NAME, Key=FILE_NAME)
    data_df = pd.read_csv(io.BytesIO(obj['Body'].read()))
    # Strip all extra spaces
    data_df = data_df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    data_df = data_df.set_index('ID')
    data_dict = data_df.to_dict('Index')
    return data_dict
