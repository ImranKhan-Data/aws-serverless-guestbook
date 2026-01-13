import json
import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('GuestBook')

def lambda_handler(event, context):
    # Get the current time
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Parse the message
    try:
        if 'body' in event:
            body_data = json.loads(event['body'])
            message_content = body_data.get('message', 'Hello from Lambda')
        else:
            message_content = event.get('message', 'Hello from Lambda')
    except Exception as e:
        message_content = "Error parsing message"

    # Save to DynamoDB
    try:
        table.put_item(Item={
            'TransactionId': now,
            'Message': message_content
        })
        
       
        # We must explicitly send these headers back to the browser
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
            },
            'body': json.dumps(f'Success! Saved message: "{message_content}" to DynamoDB')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
            },
            'body': json.dumps(f'Error saving to database: {str(e)}')
        }