import boto3
import os

def download_all_previous_versions(bucket_name, key):
    s3_client = boto3.client('s3')

    # response = s3_client.list_object_versions(Bucket=bucket_name, Prefix=key)
    response = s3_client.list_object_versions(Bucket=bucket_name, Prefix=key)


    versions = response.get('Versions', [])

    if len(versions) >= 2:
        for version in versions[1:]:
            key = version['Key']
            version_id = version['VersionId']
            file_name = f"previous_{version_id}_{os.path.basename(key)}"
            # version_id = version['VersionId']
            # file_name = f"previous_{version_id}_{os.path.basename(key)}"
            # s3_client.download_file(bucket_name, key, file_name, ExtraArgs={'VersionId': version_id})
            s3_client.download_file(bucket_name, key, file_name, ExtraArgs={'VersionId': version_id})

            print(f"Downloaded previous version: {file_name}")
    else:
        print("No previous versions found.")
 
# Usage
bucket_name = 'chrone-sp-website'
key = 'ChIJN6IdiPvJ5YgR9aP8hth_onE'

download_all_previous_versions(bucket_name, key)