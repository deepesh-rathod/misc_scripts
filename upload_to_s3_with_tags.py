import boto3
from botocore.exceptions import NoCredentialsError


def upload_to_s3(file_name, bucket, object_name=None, tags=None):
    """
    Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :param tags: Dictionary of tags to add to the object
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Convert tags dictionary to a string format
    tag_string = (
        "&".join([f"{key}={value}" for key, value in tags.items()]) if tags else ""
    )

    # Upload the file
    s3_client = boto3.client("s3")
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)

        if tags:
            s3_client.put_object_tagging(
                Bucket=bucket,
                Key=object_name,
                Tagging={"TagSet": [{"Key": k, "Value": v} for k, v in tags.items()]},
            )

        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False


# Example usage
file_name = "/Users/office/Desktop/db_schema.png"
bucket_name = "gmb-sp-image-bank"
object_name = "fb195d70-a296-4240-9bc1-4baaa90ca62a/db_schema.png"  # Optional, can be different from file_name
tags = {"destination": "GBP-WEBSITE", "source": "USER"}  # Optional


uploaded = upload_to_s3(file_name, bucket_name, object_name, tags)
if uploaded:
    print("Upload successful")
else:
    print("Upload failed")
