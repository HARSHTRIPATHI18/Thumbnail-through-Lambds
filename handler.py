import boto3
from PIL import Image
import io

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Extract bucket & object info from event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    print(f"Processing file: {key} from bucket: {bucket}")

    # Skip if this is already a thumbnail
    if key.startswith("thumbnails/"):
        return {"statusCode": 200, "body": "Skipped thumbnail image"}

    # Download the original image
    response = s3.get_object(Bucket=bucket, Key=key)
    image_content = response['Body'].read()
    img = Image.open(io.BytesIO(image_content))

    # Create thumbnail (128x128)
    img.thumbnail((128, 128))

    # Save thumbnail to memory
    buffer = io.BytesIO()
    img.save(buffer, 'JPEG')
    buffer.seek(0)

    # New key for thumbnail
    thumb_key = key.replace("uploads/", "thumbnails/")

    # Upload thumbnail to S3
    s3.put_object(Bucket=bucket, Key=thumb_key, Body=buffer, ContentType='image/jpeg')

    print(f"Thumbnail created: {thumb_key}")
    return {"statusCode": 200, "body": f"Thumbnail created at {thumb_key}"}
