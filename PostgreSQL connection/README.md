# API Endpoints

## Register a New User

### Endpoint: POST /register

Request Body:

```
{
  "login": "john_doe",

  "email": "john@example.com",

  "password": "securepassword"
}
```

Response:

```
{

  "message": "User registered successfully"

}
```

## Login and Get Access Token

### Endpoint: POST /login

Request Body:

```
{

  "login": "john_doe",

  "password": "securepassword"

}
```

Response:

```
{
  "message": "Login successful",
  "access_token": "your.jwt.token"
}
```

### If the login exists:

Response:

```
{
    "error": "Login already exists"
}
```
