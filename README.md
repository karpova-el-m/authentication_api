# User Authentication and Authorization System

## Objective

Develop a REST API for user authentication and authorization using Django and Django REST Framework. The system supports user registration, authentication, token refresh, logout, and allows users to retrieve and update their personal information. Authentication utilizes Access and Refresh tokens.

## Features

* __User Registration:__ Endpoint to register new users with email and password.
* __Authentication:__ Obtain Access and Refresh tokens using email and password.
* __Token Refresh:__ Refresh Access tokens using valid Refresh tokens.
* __Logout:__ Invalidate Refresh tokens upon user logout.
* __Personal Information:__ Retrieve and update user details.

## Technologies Used

* __Backend:__ Django, Django REST Framework
* __Authentication:__ JSON Web Tokens (JWT) for Access tokens; UUID for Refresh tokens
* __Configuration Management:__ django-constance for token lifetimes
* __Testing:__ Unit and integration tests for API endpoints

## Setup and Installation

* ### Clone the Repository:
```
git clone https://github.com/karpova-el-m/authentication_api
cd authentication_api
```

* ### Create and Activate Virtual Environment:
```
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

* ### Install Dependencies:
```
pip install -r requirements.txt
```

* ### Apply Migrations:
```
python manage.py migrate
```

* ### Run the Development Server:
```
python manage.py runserver
```

## Running Tests
* ### To run the tests:
```
python manage.py test
```
## API Endpoints

* __User Registration:__ POST /api/register/
* __Authentication:__ POST /api/login/
* __Token Refresh:__ POST /api/refresh/
* __Logout:__ POST /api/logout/
* __Retrieve Personal Information:__ GET /api/me/
* __Update Personal Information:__ PUT /api/me/

## Endpoints Description

### User Registration

```
Endpoint: /api/register/
Method: POST
Body:
{
  "password": "password",
  "email": "user@example.com"
}
Response:
{
  "id": 1,
  "email": "user@example.com"
}
Curl Command:

curl -X POST http://localhost:8000/api/register/ -d '{"password": "password", "email": "user@example.com"}' -H "Content-Type: application/json"
```

### Authentication (Obtaining Access and Refresh Token)

```
Endpoint: /api/login/
Method: POST
Body:
{
  "email": "user@example.com",
  "password": "password"
}
Response:
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "d952527b-caef-452c-8c93-1100214f82e5"
}
Curl Command:

curl -X POST http://localhost:8000/api/login/ -d '{"email": "user@example.com", "password": "password"}' -H "Content-Type: application/json"
```

### Access Token Refresh

```
Endpoint: /api/refresh/
Method: POST
Body:
{
  "refresh_token": "d952527b-caef-452c-8c93-1100214f82e5"
}
Response:
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eb0464c2-ed6e-4346-a709-042c33946154"
}
Curl Command:

curl -X POST http://localhost:8000/api/refresh/ -d '{"refresh_token": "eb0464c2-ed6e-4346-a709-042c33946154"}' -H "Content-Type: application/json"
```

### Logout (Invalidating Refresh Token)

```
Endpoint: /api/logout/
Method: POST
Body:
{
  "refresh_token": "eb0464c2-ed6e-4346-a709-042c33946154"
}
Response:
{
  "success": "User logged out."
}
Curl Command:

curl -X POST http://localhost:8000/api/logout/ -d '{"refresh_token": "eb0464c2-ed6e-4346-a709-042c33946154"}' -H "Content-Type: application/json"
```

### Retrieving Personal Information

```
Endpoint: /api/me/
Method: GET
Header:
Authorization: Bearer <access_token>
Response:
{
  "id": 1,
  "username": "",
  "email": "user@example.com"
}
Curl Command:

curl -X GET http://localhost:8000/api/me/ -H "Authorization: Bearer <access_token>"
```

### Updating Personal Information

```
Endpoint: /api/me/
Method: PUT
Header:
Authorization: Bearer <access_token>
Body:
{
  "username": "John Smith"
}
Response:
{
  "id": 1,
  "username": "John Smith",
  "email": "user@example.com"
}
Curl Command:

curl -X PUT http://localhost:8000/api/me/ -d '{"username": "John Smith"}' -H "Content-Type: application/json" -H "Authorization: Bearer <access_token>"
```

## Developer

__Karpova Elena__ - https://github.com/karpova-el-m

__Telegram__ - [@karpova_el_m](https://t.me/karpova_el_m)