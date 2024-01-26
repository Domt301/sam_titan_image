import json
import logging
import boto3
from botocore.exceptions import ClientError
import base64

logger = logging.getLogger(__name__)

brt = boto3.client('bedrock-runtime', region_name='us-east-1' )

 
def lambda_handler(event, context):
    if 'body' not in event or not event['body']:
        return {
            'statusCode': 400,
            'body': json.dumps('No body provided')
        }
    try:
        body = json.loads(event['body'])
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'body': json.dumps('Invalid JSON in body')
        }
    if 'prompt' not in body:
        return {
            'statusCode': 400,
            'body': json.dumps('Prompt needs to be passed in the body')
        }
    prompt = body['prompt']
    chat_response = invoke_llm(prompt)
    res = ({'response': chat_response})
    return {
        'statusCode': 200,
        'body': json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
             "Access-Control-Allow-Methods": "POST"
        },
    }

 

def invoke_llm(prompt):
    try:
        body = json.dumps({"prompt": prompt })
        modelId = 'ai21.j2-mid-v1'
        accept = 'application/json'
        contentType = 'application/json'
        response = brt.invoke_model(body=body, modelId=modelId, accept=accept, contentType=contentType)
        response_body = json.loads(response.get('body').read())
        logger.info(response_body)
        response_content = response_body.get('completions')[0].get('data').get('text').replace('\n', '')
        logger.info(response_content)
        return response_content
    except Exception as e:
        logger.error(e)
        raise e
