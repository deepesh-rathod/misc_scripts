import boto3

def copy_folder_contents(source_bucket, source_folder, destination_bucket, destination_folder):
    s3 = boto3.client('s3')
    paginator = s3.get_paginator('list_objects_v2')

    # List all objects in the source folder
    operation_parameters = {
        'Bucket': source_bucket,
        'Prefix': source_folder
    }
    page_iterator = paginator.paginate(**operation_parameters)

    # Copy each object to the destination folder
    for page in page_iterator:
        if 'Contents' in page:
            for obj in page['Contents']:
                old_key = obj['Key']
                new_key = old_key.replace(source_folder, destination_folder, 1)

                copy_source = {
                    'Bucket': source_bucket,
                    'Key': old_key
                }

                s3.copy_object(
                    CopySource=copy_source,
                    Bucket=destination_bucket,
                    Key=new_key
                )

# Usage example
source_bucket = 'chrone-sp-website'
source_folder = 'ChIJzVZ2FmWp2YgRoZhP2sNO7OQ'
destination_bucket = 'chrone-sp-website'
destination_folder = 'b5943ee7-2bc5-4302-87c9-71402eb30970'

copy_folder_contents(source_bucket, source_folder, destination_bucket, destination_folder)
