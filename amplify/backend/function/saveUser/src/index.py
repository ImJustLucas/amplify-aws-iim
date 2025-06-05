import json
import boto3
import uuid
import os
import re

from boto3.dynamodb.conditions import Key, Attr

def handler(event, context):

  if event.get('httpMethod') and event['httpMethod'] != 'POST':
    return {
      'statusCode': 405,
      'body': json.dumps({'message': 'Method Not Allowed, only POST is accepted'})
    }

  body = json.loads(event['body'])
  name = body.get('name')
  email = body.get('email')
  if not name or not email:
    return {
      'statusCode': 400,
      'body': json.dumps({'message': 'Missing name or email'})
    }

  email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
  if not re.match(email_regex, email):
    return {
      'statusCode': 400,
      'body': json.dumps({'message': 'Invalid email format'})
    }

  table_name = os.environ['STORAGE_USERS_NAME']
  dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
  table = dynamodb.Table(table_name)

  response = table.query(
    IndexName='emails',
    KeyConditionExpression=Key('email').eq(email)
  )
  if response['Items']:
    return {
      'statusCode': 409,
      'body': json.dumps({'message': 'This email is already used.'})
    }

  table.put_item(Item={
    'id': str(uuid.uuid4()),
    'name': name,
    'email': email,
  })

  return {
    'statusCode': 200,
    'body': json.dumps({'message': 'User created successfully.'})
  }