import boto3
import random

session = boto3.Session(
    aws_access_key_id="AKIASQ6IOBTRNZ2TKNHO",
    aws_secret_access_key="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",
)
s3 = session.resource('s3')
place_ids = ["ChIJfzqhWyB4ToYRkCQazMgnXj4"]
for place_id in place_ids:
    i = random.randint(1,23)
    banner = f"Skin Care Clinic/{i}.webp"
    copy_source = {
        'Bucket': 'chrone-website',
        'Key': banner
        }
    bucket = s3.Bucket('chrone-website')
    bucket.copy(copy_source, f'{place_id}/banner.webp')
    j = random.randint(1,23)
    services = f"Skin Care Clinic/{j}.webp"
    copy_source = {
        'Bucket': 'chrone-website',
        'Key': services
        }
    bucket = s3.Bucket('chrone-website')
    bucket.copy(copy_source, f'{place_id}/services.webp')
print(0)