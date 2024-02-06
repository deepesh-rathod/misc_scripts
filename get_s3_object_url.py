import boto3
from urllib.parse import quote_plus


def get_s3_object_public_urls(bucket_name, folder_path):
    # Create an S3 client
    s3_client = boto3.client("s3")

    # Ensure the folder path ends with '/'
    if not folder_path.endswith("/"):
        folder_path += "/"

    # List objects within the specified folder
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=folder_path)

    # Initialize the list to store URLs
    public_urls = []

    # Check if the response contains 'Contents'
    if "Contents" in response:
        for content in response["Contents"]:
            # Construct the public URL
            object_key = content["Key"]
            public_url = f"https://{bucket_name}.s3.amazonaws.com/{object_key}"
            public_urls.append(public_url)

    return public_urls


# Usage
bucket_name = "chroneapp"
folder_path = "campaign-flyer-template/"
public_urls = get_s3_object_public_urls(bucket_name, folder_path)
for url in public_urls:
    print(url + "\n")
