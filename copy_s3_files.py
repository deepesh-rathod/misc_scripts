import boto3
import requests
from sqlalchemy import true
from io import BytesIO
from urllib import parse


def get_all_s3_objects(bucket_name, folder_name):
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(bucket_name)

    files = []
    for obj in bucket.objects.filter(Prefix=folder_name):
        if obj.key != folder_name:  # Exclude the folder itself
            files.append(obj.key)

    return files


def delete_files_with_min(bucket_name, folder_name):
    s3 = boto3.client("s3")

    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=folder_name)
    objects_to_delete = []

    for obj in response.get("Contents", []):
        key = obj["Key"]
        if "_min" in key:
            objects_to_delete.append({"Key": key})

    if len(objects_to_delete) > 0:
        response = s3.delete_objects(
            Bucket=bucket_name, Delete={"Objects": objects_to_delete}
        )
        if "Errors" in response:
            print("Failed to delete some objects:")
            for error in response["Errors"]:
                print(f"Object Key: {error['Key']}, Error Code: {error['Code']}")
        else:
            print("All objects with '_min' in their file name have been deleted.")
    else:
        print("No objects with '_min' in their file name found.")


def copy_file_with_new_name(bucket_name, folder_name, old_key, new_key):
    s3 = boto3.client("s3")

    object_url = "https://d15e7bk5l2jbs8.cloudfront.net/" + old_key

    resp = requests.get(object_url, stream=True)
    img = BytesIO(resp.content)
    # print(0)

    copy_source = {"Bucket": bucket_name, "Key": old_key}
    tags = {"key1": "value1", "key2": "value2"}

    s3.upload_file(
        img,
        Bucket="gmb-sp-image-bank",
        Key=new_key,
        ExtraArgs={"Tagging": parse.urlencode(tags)},
    )
    print(f"File '{old_key}' copied to '{new_key}' successfully.")


# Replace 'your-bucket-name' and 'your-folder-name' with the actual names
bucket_name = "chrone-sp-website"
folder_name = "ChIJL1wNMU-fj4ARzML8e5Pgdy4/gallery"

# delete_files_with_min(bucket_name, folder_name)
file_list = get_all_s3_objects(bucket_name, folder_name)

# Print the list of files in the S3 folder
for file_name in file_list:
    if "_new" in file_name:
        new_file_name = file_name.replace(".webp", "_min.webp")
        copy_file_with_new_name(
            bucket_name,
            folder_name,
            file_name,
            "fb195d70-a296-4240-9bc1-4baaa90ca62a/" + new_file_name.split("/")[-1],
        )
        print(f"{file_name} : {new_file_name}")
