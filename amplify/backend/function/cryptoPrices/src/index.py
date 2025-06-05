import json
import requests
import boto3
from datetime import datetime
from decimal import Decimal

# Configuration DynamoDB
REGION = 'eu-west-1'
TABLE_NAME = 'cryptoPrices-lucas'   

dynamodb = boto3.resource('dynamodb', region_name=REGION)
table = dynamodb.Table(TABLE_NAME)

API_URL = "https://api.coingecko.com/api/v3/coins/markets"
MAX_PAGE = 1   


def handler(event, context):
    print('received event:')
    print(event)
    timestamp = datetime.utcnow().isoformat()

    try:
        for page in range(1, MAX_PAGE + 1):
            params = {
                "vs_currency": "usd",
                "order": "market_cap_desc",
                "per_page": 50,
                "page": page,
                "sparkline": False
            }
            response = requests.get(API_URL, params=params)
            data = response.json()

            for coin in data:
                table.put_item(
                    Item={
                        "crypto_id": coin["id"],
                        "timestamp": timestamp,
                        "name": coin["name"],
                        "symbol": coin["symbol"],
                        "price": Decimal(str(coin["current_price"]))
                    }
                )

        return {
            "statusCode": 200,
            "headers": {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            "body": json.dumps({"message": "Crypto prices saved successfully"})
        }
    except Exception as e:
        print('Error:', str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }


 