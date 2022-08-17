"""
 imagedataSerializer:  a Lambda function to serialize the image data to be ready for classification.
"""
import json
import boto3
import base64

s3 = boto3.client('s3')

def lambda_handler(event, context):
    """A function to serialize target data from S3"""
    
    # Get the s3 address from the Step Function event input
    key = event["s3_key"]
    bucket = event["s3_bucket"]
    
    # Download the data from s3 to /tmp/image.png
    boto3.resource('s3').Bucket(bucket).download_file(key, "/tmp/image.png")
    
    # We read the data from the file
    with open("/tmp/image.png", "rb") as f:
        image_data = base64.b64encode(f.read())

    # Pass the data back to the Step Function along with a success status code
    print("Event:", event.keys())
    return {
        'statusCode': 200,
        'body': {
            "image_data": image_data,
            "s3_bucket": bucket,
            "s3_key": key,
            "inferences": []
        }
    }







"""
ImageClassifier : a function to predict image class.
"""
import os
import io
import boto3
import json
import base64

ENDPOINT_NAME = 'image-classification-2022-08-12-15-11-08-809'

runtime= boto3.client('runtime.sagemaker')

def lambda_handler(event, context):
    
    # Decode the image data
    image = base64.b64decode(event["body"]["image_data"])
    
    # Make a prediction:
    response = runtime.invoke_endpoint(EndpointName=ENDPOINT_NAME,
                                       ContentType='image/png',
                                       Body=image)
    
    # We return the data back to the Step Function    
    event["body"]["inferences"] = json.loads(response['Body'].read().decode('utf-8'))
    return{
        'statusCode': 200,
        'body': {
            "image_data": event["body"]['image_data'],
            "s3_bucket": event["body"]['s3_bucket'],
            "s3_key": event["body"]['s3_key'],
            "inferences": event["body"]['inferences'],
        }
    }








"""
InferenceConfidenceFilter : a function to fiter inference results based on confidence
"""
import json


THRESHOLD = .9

def lambda_handler(event, context):
    # Get the inferences from the event body
    inferences = event["body"]["inferences"]
    
    # Check if any values in any inferences are above the desired threshold
    meets_threshold = (max(inferences) > THRESHOLD)
    
    # If the threshold is met, pass our data back to be captured out of the
    # Step Function, else... end the Step Function with an error
    if meets_threshold:
        pass
    else:
        raise("THRESHOLD_CONFIDENCE_NOT_MET")

    return {
        'statusCode': 200,
        'body': event
    }