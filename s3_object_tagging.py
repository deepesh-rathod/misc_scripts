import boto3


def tag_objects_in_folder(bucket_name, folder_prefix, tags):
    """
    Apply tags to all objects within a specific folder in an S3 bucket.

    :param bucket_name: str, the name of the S3 bucket.
    :param folder_prefix: str, the folder prefix (path).
    :param tags: dict, tags to apply in the format {'Key': 'Value'}.
    """

    # Initialize S3 client
    s3_client = boto3.client("s3")

    # Convert tags dict to the format required by S3
    tag_set = [{"Key": key, "Value": value} for key, value in tags.items()]

    # List objects within the specified folder
    paginator = s3_client.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=bucket_name, Prefix=folder_prefix):
        for obj in page.get("Contents", []):
            # Apply tags to each object
            s3_client.put_object_tagging(
                Bucket=bucket_name, Key=obj["Key"], Tagging={"TagSet": tag_set}
            )
            # response = s3_client.get_object_tagging(Bucket=bucket_name, Key=obj["Key"])
            # for tag in response["TagSet"]:
            #     print(tag["Key"], tag["Value"])


# Example usage
bucket_name = "chrone-sp-website"
folder_prefix = "1fc1c04f-8ab6-4bb0-abe1-6c5938df94e4/gallery/"  # Ensure the folder name ends with '/'
tags = {"backfill": "true", "destination": "website", "section": "gallery"}

tag_objects_in_folder(bucket_name, folder_prefix, tags)
