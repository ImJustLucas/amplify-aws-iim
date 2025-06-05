import json
import boto3
import os
from boto3.dynamodb.conditions import Key
import uuid

def handler(event, context):
  print('received event:')
  print(event)
  
  params = event.get('queryStringParameters', {}) or {}
  user_id = params.get('id')
  email = params.get('email')

  if not user_id and not email:
    return {
      'statusCode': 400,
      'body': json.dumps({'message': 'You must provide either id or email as query parameter.'})
    }

  table_name = os.environ['STORAGE_USERS_NAME']
  dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
  table = dynamodb.Table(table_name)

  try:
    if user_id:
      response = table.get_item(Key={'id': user_id})
      user = response.get('Item')
      if user:
        return {
          'statusCode': 200,
          'body': json.dumps(user)
        }
      else:
        return {
          'statusCode': 404,
          'body': json.dumps({'message': f'User not found with ID: {user_id}', 'id': user_id})
        }
      
    elif email:

      response = table.query(
        IndexName='emails',
        KeyConditionExpression=Key('email').eq(email)
      )
      items = response.get('Items', [])
      if items:
        return {
          'statusCode': 200,
          'body': json.dumps(items[0])
        }
      else:
        return {
          'statusCode': 404,
          'body': json.dumps({'message': f'User not found with email: {email}', 'email': email})
        }
      
  except Exception as e:
    print('Error:', str(e))
    return {
      'statusCode': 500,
      'body': json.dumps({'message': 'Internal server error', 'error': str(e)})
    } 