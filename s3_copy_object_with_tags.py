import boto3
import uuid


def get_media_extension(key):
    return key.split(".")[-1]


def get_uid(key):
    return key.split("/")[0]


def get_new_key(old_key):
    temp_id = str(uuid.uuid4())
    ext = get_media_extension(old_key)
    uid = get_uid(old_key)
    return uid + "/" + temp_id + "." + ext


def copy_object_with_tags(destination_bucket, source_bucket, folder_prefix):
    s3_client = boto3.client("s3")

    paginator = s3_client.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=source_bucket, Prefix=folder_prefix):
        for obj in page.get("Contents", []):
            new_key = get_new_key(obj["Key"])

            response = s3_client.copy_object(
                Bucket=destination_bucket,
                CopySource={"Bucket": source_bucket, "Key": obj["Key"]},
                Key=new_key,
                TaggingDirective="COPY",
            )
            print(0)


destination_bucket = "gmb-sp-image-bank"
source_bucket = "chrone-sp-website"
folder_prefix = "1fc1c04f-8ab6-4bb0-abe1-6c5938df94e4/gallery/"

copy_object_with_tags(destination_bucket, source_bucket, folder_prefix)
