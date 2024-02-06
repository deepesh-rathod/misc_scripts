import boto3

def rename_files_in_s3_folder(bucket_name, folder_name, new_prefix):
    # Create an S3 client
    s3 = boto3.client('s3')

    # List objects in the specified S3 folder
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=folder_name)

    # Check if the folder is empty
    if 'Contents' not in response:
        print(f"No objects found in '{folder_name}' in bucket '{bucket_name}'.")
        return

    # Rename files
    for obj in response['Contents']:
        old_key = obj['Key']
        if old_key.startswith(folder_name):
            # Extract the file name from the old key
            file_name = old_key.split('/')[-1]

            # Combine the folder name and the new prefix to create the new key
            new_file_name = file_name.replace("_new","")
            new_key = f"{folder_name}{new_file_name}"

            # Copy the object to the new key
            s3.copy_object(
                Bucket=bucket_name,
                CopySource={'Bucket': bucket_name, 'Key': old_key},
                Key=new_key
            )

            # Delete the old object
            s3.delete_object(Bucket=bucket_name, Key=old_key)

            print(f"Renamed '{old_key}' to '{new_key}' in bucket '{bucket_name}'.")

if __name__ == "__main__":
    # Replace with your S3 bucket name, folder name, and new prefix
    bucket_name = "chrone-sp-website"
    folder_name = "409df862-0a64-4ae4-bf81-23664d9e032c/gallery/"
    new_prefix = "409df862-0a64-4ae4-bf81-23664d9e032c/gallery/"

    rename_files_in_s3_folder(bucket_name, folder_name, new_prefix)
