import json
import logging
import boto3
from botocore.exceptions import ClientError
import base64

logger = logging.getLogger(__name__)

bedrock_runtime_client = boto3.client('bedrock-runtime', region_name='us-east-1' )

 
def lambda_handler(event, context):
    # Check if there is a body in the event
    if 'body' not in event or not event['body']:
        return {
            'statusCode': 400,
            'body': json.dumps('No body provided')
        }

    # Parse the body
    try:
        body = json.loads(event['body'])
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'body': json.dumps('Invalid JSON in body')
        }

    # Check if 'prompt' is in the body
    if 'prompt' not in body:
        return {
            'statusCode': 400,
            'body': json.dumps('Prompt needs to be passed in the body')
        }

    prompt = body['prompt']
    image_data = invoke_titan_image(prompt)
    
    result_array = []
    for image in image_data:
        result_array.append({'base64': image})
    
    return {
        'statusCode': 200,
        'body': json.dumps(result_array),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
             "Access-Control-Allow-Methods": "POST"
        },
    }

 



def invoke_titan_image(prompt, style_preset=None):
        try:
            body = json.dumps(
                {
                    "taskType": "TEXT_IMAGE",
                    "textToImageParams": {
                        "text":prompt,   # Required
            #           "negativeText": "<text>"  # Optional
                    },
                    "imageGenerationConfig": {
                        "numberOfImages": 1,   # Range: 1 to 5 
                        "quality": "premium",  # Options: standard or premium
                        "height": 768,         # Supported height list in the docs 
                        "width": 1280,         # Supported width list in the docs
                        "cfgScale": 7.5,       # Range: 1.0 (exclusive) to 10.0
                        "seed": 42             # Range: 0 to 214783647
                    }
                }
            )
            response = bedrock_runtime_client.invoke_model(
                body=body, 
                modelId="amazon.titan-image-generator-v1",
                accept="application/json", 
                contentType="application/json"
            )

            response_body = json.loads(response["body"].read())
            base64_image_data = response_body["images"]

            return base64_image_data

        except ClientError:
            logger.error("Couldn't invoke Titan Image Generator Model")
            raise