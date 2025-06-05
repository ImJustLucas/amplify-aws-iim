# 🚀 Crypto Price Tracker Project

![AWS](https://img.shields.io/badge/AWS-Amplify-orange)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![DynamoDB](https://img.shields.io/badge/Database-DynamoDB-yellow)

## 📋 Overview

A comprehensive cryptocurrency tracking and user management platform built with AWS Amplify. This system fetches real-time cryptocurrency prices, stores historical data, and provides user authentication.

## 🏗️ Architecture

```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│  API Gateway │────▶│Lambda Functions│────▶│   DynamoDB   │
└─────────────┘     └──────────────┘     └──────────────┘
       │                   │                    │
       │                   ▼                    │
       │             ┌──────────┐               │
       └────────────▶│ S3 Bucket│◀──────────────┘
                     └──────────┘
```

## 🔌 API Endpoints

### Crypto API

#### `GET /export`

- **Description**: Exports cryptocurrency price data from DynamoDB to S3
- **Response**:
  ```json
  {
    "message": "Export successful",
    "url": "https://pre-signed-s3-url",
    "file_key": "exports/crypto_YYYY-MM-DDTHH-MM-SS.json"
  }
  ```

### Users API

#### `POST /save-user`

- **Description**: Creates a new user
- **Request Body**:
  ```json
  {
    "name": "User Name",
    "email": "user@example.com"
  }
  ```
- **Response**:
  ```json
  {
    "message": "Utilisateur créé avec succès."
  }
  ```

#### `GET /get-user`

- **Query Parameters**: `id` OR `email`
- **Response**:
  ```json
  {
    "id": "uuid",
    "name": "User Name",
    "email": "user@example.com"
  }
  ```

## ⚙️ Lambda Functions

| Function       | Description                       | Trigger     | Dependencies |
| -------------- | --------------------------------- | ----------- | ------------ |
| `signeData`    | Exports cryptocurrency data to S3 | API Gateway | DynamoDB, S3 |
| `cryptoPrices` | Fetches prices from CoinGecko API | Scheduled   | DynamoDB     |
| `saveUser`     | Creates new users                 | API Gateway | DynamoDB     |
| `getUser`      | Retrieves user data               | API Gateway | DynamoDB     |

## 💾 Storage Resources

### DynamoDB Tables

#### `cryptoPrices`

- **Partition Key**: `crypto_id` (string)
- **Sort Key**: `timestamp` (string)
- **Schema**:
  - `crypto_id`: string
  - `timestamp`: string
  - `name`: string
  - `symbol`: string
  - `price`: number

#### `users`

- **Partition Key**: `id` (string)
- **GSI**: `emails` (partition key: email)
- **Schema**:
  - `id`: string (UUID)
  - `name`: string
  - `email`: string

### S3 Bucket

#### `cryptostorage`

- **Access**:
  - Guest: READ
  - Authenticated: CREATE_AND_UPDATE, READ, DELETE
- **Content**: Exported cryptocurrency data files

## 📱 Mobile Application

### Features

- User authentication
- Real-time cryptocurrency price tracking
- Data export capabilities
- User profile management

### Authentication Flow

```
┌──────────┐     ┌─────────┐     ┌──────────┐
│  Sign Up  │────▶│ Cognito │────▶│ Confirmed│
└──────────┘     └─────────┘     └──────────┘
      │               ▲               │
      │               │               │
      ▼               │               ▼
┌──────────┐     ┌─────────┐     ┌──────────┐
│   Email   │────▶│Verification│──▶│  Sign In │
└──────────┘     └─────────┘     └──────────┘
```

## 🔧 Usage Examples

### Export Cryptocurrency Data

```bash
curl -X GET https://your-api-endpoint/export
```

### Create a New User

```bash
curl -X POST https://your-api-endpoint/save-user \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com"}'
```

### Get User by ID

```bash
curl -X GET https://your-api-endpoint/get-user?id=12345-uuid
```

### Get User by Email

```bash
curl -X GET https://your-api-endpoint/get-user?email=john@example.com
```

## 🔒 Security

- Authentication via AWS Cognito
- Secure S3 bucket access
- API permissions configured through IAM

## 📊 Data Flow

1. CoinGecko API → Lambda (`cryptoPrices`) → DynamoDB (`cryptoPrices`)
2. API Request → Lambda (`signeData`) → DynamoDB → S3 → Pre-signed URL
3. Registration → API → Lambda (`saveUser`) → DynamoDB (`users`)
4. Login → Cognito → JWT Token → Authenticated API Access

## 🚀 Deployment

The application is deployed using AWS Amplify CLI:

```bash
amplify push
```

## 🧵 Troubleshooting

- Check CloudWatch Logs for Lambda execution issues
- Verify IAM permissions for cross-service access
- Ensure DynamoDB capacity is sufficient for read/write operations
- For authentication issues, check Cognito user pool configuration
