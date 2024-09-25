# Machine-to-Machine Authentication with Client Credentials Grant

This section demonstrates the OAuth 2.0 Client Credentials flow, which is used for machine-to-machine authentication without user involvement.

<img width="782" alt="image" src="https://github.com/user-attachments/assets/e9f674b0-c75d-4803-b5ac-7a92c9909b68">

The above diagram illustrates the OAuth 2.0 Client Credentials flow implemented in this project:

1. A client application (simulated by Postman acting as a Cron Job) requests an access token from the Okta Authorization Server using the Client Credentials grant type.
2. Okta's Authorization Server validates the client credentials and issues an access token.
3. The client then calls the FakeBook API with the obtained access token.
4. The FakeBook API validates the token by retrieving the public signing keys from Okta's JSON Web Key Set (JWKS) endpoint.
5. If the token is valid and has the required scopes, the API processes the request and returns the response.

This setup demonstrates a real-world scenario where a backend service or cron job needs to access an API securely without user interaction. The FakeBook API provides endpoints for managing a collection of books, with different access levels based on OAuth scopes:
- Reading book information requires the 'fakebookapi.read' scope
- Adding new books requires the 'fakebookapi.admin' scope

By implementing this flow, we ensure that only authenticated and authorized clients can access our API, with fine-grained control over permissions using OAuth scopes.

## Project Overview

This project demonstrates the implementation of OAuth 2.0 Client Credentials flow using Okta as the authorization server. The setup involves three main components:

1. **FakeBook API Server**: A Flask-based API that manages book information and requires OAuth 2.0 token authentication.

2. **Okta Client Application**: An application registered in Okta that represents the client seeking access to the FakeBook API.

3. **Postman (Emulating a Cron Job)**: Used to simulate a backend service or scheduled job that interacts with the FakeBook API using OAuth 2.0 tokens.

Below, we'll go through the setup and usage of each of these components in detail.

## Okta Developer Account Setup

To use this API with Okta as the authorization server, you need to set up an Okta developer account and create an application. Follow these steps:

1. Sign up for an Okta Developer Account:
   - Go to [https://developer.okta.com/](https://developer.okta.com/)
   - Click on "Sign Up" and complete the registration process

2. Create a new Application:
   - Log in to your Okta developer dashboard
   - Navigate to Applications > Create App Integration
   - Select "API Services" as the type of application
   - Click "Next"

3. Configure the Application:
   - Name: Enter "FakeBook Cron" (or any name you prefer)
   - Grant type: Ensure "Client Credentials" is selected
   - Click "Save"

4. Assign API Scopes:
   - In your new application's settings, go to the "Scopes" tab
   - Add the following scopes:
     - `fakebookapi.read`
     - `fakebookapi.admin`
   - If these scopes don't exist, you may need to create them in your Authorization Server settings

5. Copy Credentials:
   - In the "General" tab of your application, you will find the "Client ID"
   - Click on "Show" next to "Client secret" to reveal the secret
   - Copy both the Client ID and Client secret; you'll need these for authentication in Postman

6. Configure Your Authorization Server:
   - Go to Security > API > Authorization Servers
   - Select your authorization server (or create a new one if needed)
   - In the "Scopes" tab, add the `fakebookapi.read` and `fakebookapi.admin` scopes if they don't already exist

7. Update Your Application:
   - https://dev-45134456.okta.com/oauth2/default/.well-known/openid-configuration
   - Open the `app.py` file in your project
   - It will look similar to below. Replace the `OKTA_JWKS_URI` with your Okta domain's JWKS URI:
     ```python
     OKTA_JWKS_URI = 'https://{yourOktaDomain}/oauth2/default/v1/keys'
     ```
   - Replace `{yourOktaDomain}` with your actual Okta domain (e.g., `dev-1234567.okta.com`)

Now you're ready to use these credentials in Postman to obtain access tokens from Okta and test your FakeBook API.

## FakeBook API

### Introduction

FakeBook API is a Flask-based RESTful API that demonstrates OAuth 2.0 integration with Okta for authentication and authorization. This project showcases how to implement secure, scope-based access control for API endpoints using JSON Web Tokens (JWTs) issued by Okta.

The API provides endpoints for managing a collection of books, with different access levels based on OAuth scopes:
- Reading book information requires the 'fakebookapi.read' scope
- Adding new books requires the 'fakebookapi.admin' scope

This setup mimics real-world scenarios where different API operations require different levels of access.

<img width="800" alt="image" src="https://github.com/user-attachments/assets/7782ee33-46e8-4d9e-a5e1-715bc81112bb">


## Setup and Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- An Okta developer account

### Setting Up the Virtual Environment

1. Clone the repository:
   ```
   git clone https://github.com/your-username/fakebook-api.git
   cd fakebook-api
   ```

2. Create a virtual environment:
   ```
   python3 -m venv venv
   ```

3. Activate the virtual environment:
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```
   - On Windows:
     ```
     venv\Scripts\activate
     ```

4. Install the required packages:
   ```
   pip install flask flask-restful pyjwt[crypto] cryptography
   ```

### Configuration

1. Open `app.py` and replace the `OKTA_JWKS_URI` with your Okta domain's JWKS URI:
   ```python
   OKTA_JWKS_URI = 'https://your-okta-domain.okta.com/oauth2/default/v1/keys'
   ```
   JWKS endpoint URI can also be obtained through the below URL (double check this to make sure you are using the correct URI):
   - https://dev-45134456.okta.com/oauth2/default/.well-known/openid-configuration
   - Replace `dev-45134456.okta.com` with your actual Okta domain (e.g., `dev-1234567.okta.com`)
     
2. Ensure your Okta application is set up with the correct scopes ('fakebookapi.read' and 'fakebookapi.admin'). 

## Running the Application

1. Ensure your virtual environment is activated.

2. Run the Flask application:
   ```
   python app.py
   ```

3. The server will start, typically on `http://127.0.0.1:5000/`.

## Code Explanation

### Main Components

1. **Flask and Flask-RESTful Setup** (Lines 1-5, 10-13):
   The application uses Flask as the web framework and Flask-RESTful for creating RESTful APIs.
   ```python
   from flask import Flask, jsonify, request
   from flask_restful import Api, Resource
   # ...
   app = Flask(__name__)
   api = Api(app)
   ```

2. **JWT Verification** (Lines 6-7, 14-16):
   Custom JWT verification is implemented using PyJWKClient, which fetches the signing key from Okta's JWKS endpoint.
   ```python
   from jwt import PyJWKClient, decode as jwt_decode, exceptions as jwt_exceptions
   # ...
   OKTA_JWKS_URI = 'https://dev-45134456.okta.com/oauth2/default/v1/keys'
   jwks_client = PyJWKClient(OKTA_JWKS_URI)
   ```

3. **Scope-based Access Control** (Lines 40-54):
   The `require_scope` decorator checks for required scopes in the JWT claims.
   ```python
   def require_scope(required_scope):
       def decorator(fn):
           @wraps(fn)
           def wrapper(*args, **kwargs):
               # ... (scope checking logic)
           return wrapper
       return decorator
   ```

4. **Book Model and Data** (Lines 17-36):
   A simple `FakeBook` class represents book objects, with a list of books stored in memory.
   ```python
   class FakeBook:
       def __init__(self, id, title, author, cost, num_pages):
           # ... (FakeBook initialization)
   
   books = [
       FakeBook(1, "And Then There Were None", "Agatha Christie", 7.99, 300),
       # ... (more books)
   ]
   ```

5. **API Resources** (Lines 55-80):
   * `BookList`: Handles GET (list all books) and POST (add a new book) requests.
   * `Book`: Handles GET requests for individual books.
   ```python
   class BookList(Resource):
       @require_scope('fakebookapi.read')
       def get(self):
           # ... (GET logic)
   
       @require_scope('fakebookapi.admin')
       def post(self):
           # ... (POST logic)
   
   class Book(Resource):
       @require_scope('fakebookapi.read')
       def get(self, book_id):
           # ... (GET single book logic)
   ```

### Key Functions

1. **verify_jwt(token)** (Lines 25-35):
   Verifies the JWT using Okta's JWKS. It handles token expiration and invalidity.
   ```python
   def verify_jwt(token):
       try:
           signing_key = jwks_client.get_signing_key_from_jwt(token)
           decoded_token = jwt_decode(token, signing_key.key, algorithms=["RS256"], audience='api://default')
           return decoded_token
       except jwt_exceptions.ExpiredSignatureError:
           return {"message": "Token has expired"}, 401
       except jwt_exceptions.InvalidTokenError:
           return {"message": "Invalid token"}, 401
   ```

2. **require_scope(required_scope)** (Lines 40-54):
   A decorator that checks if the JWT contains the required scope for the operation.
   ```python
   def require_scope(required_scope):
       def decorator(fn):
           @wraps(fn)
           def wrapper(*args, **kwargs):
               # ... (scope checking logic)
           return wrapper
       return decorator
   ```

3. **before_request()** (Lines 85-87):
   Ensures the application remains stateless by disabling session creation.
   ```python
   @app.before_request
   def before_request():
       request.environ['werkzeug.session_interface'] = None
   ```


## Testing With Postman

You can test the API using tools like Postman or curl. This guide will walk you through the process of obtaining a JWT token from Okta and using it to interact with the FakeBook API.

### Prerequisites
- Postman or curl installed
- Your Okta developer account credentials

### Step 1 & 2: Obtain JWT Token from Okta

#### 1. Construct a Token Request for Client Credentials

**Endpoint:** `https://dev-45134456.okta.com/oauth2/default/v1/token`
**HTTP Method:** POST
**Headers:**
- Content-Type: application/x-www-form-urlencoded

**Body:**
```
grant_type=client_credentials
client_id=<your_client_id>
client_secret=<your_client_secret>
scope=fakebookapi.read
```

#### 2. Send Token Request and Extract Token

- Send the request to Okta's token endpoint
- Okta will return a JWT access token
- You can decode and inspect the token at [jwt.io](https://jwt.io)

**Note:** 
- Using `openid` as the scope will fail (Why? OpenID Connect scopes are not applicable for Client Credentials flow)
- No ID token or refresh token is provided in this flow

![Okta Token Request](https://github.com/user-attachments/assets/47782948-46c4-4865-b1da-a0a28f927ce5)

### Step 3 & 4: Use the Token with FakeBook API

#### 3. Prepare API Request

**Endpoint:** `http://localhost:5000/books/1`
**HTTP Method:** GET
**Headers:**
```
Authorization: Bearer <your_jwt_token>
```

#### 4. Send Request to FakeBook API

Send the request and observe the response. You should receive details of the book with ID 1.

![FakeBook API Request](https://github.com/user-attachments/assets/77e4e3af-d813-4182-aaae-aa87c81fe5dc)

### Step 5: Attempt to Create a Book (Expected to Fail)

**Endpoint:** `http://localhost:5000/books`
**HTTP Method:** POST
**Headers:**
```
Authorization: Bearer <your_jwt_token>
Content-Type: application/json
```
**Body:** (Example)
```json
{
        "author": "Woziek Schezcny",
        "cost": 7.99,
        "id": 6,
        "num_pages": 300,
        "title": "And Then There Were None"
    }
```

This request will fail because the access token only has the `fakebookapi.read` scope.

### Obtaining a Token with Admin Scope

To create books, you need a token with both `fakebookapi.read` and `fakebookapi.admin` scopes:

**Endpoint:** `https://dev-45134456.okta.com/oauth2/default/v1/token`
**HTTP Method:** POST
**Body:**
```
grant_type=client_credentials
client_id=<your_client_id>
client_secret=<your_client_secret>
scope=fakebookapi.read fakebookapi.admin
```

Use this new token to successfully create books via the POST /books endpoint.

### Summary of Scope Requirements

- To read books (GET /books or GET /books/<id>), the JWT token must have the 'fakebookapi.read' scope.
- To create a new book (POST /books), the JWT token must have the 'fakebookapi.admin' scope.
- If a token doesn't have the required scope, the request will be denied with a 403 error.

### Note on OpenID Connect Scopes:
If you attempt to use 'openid' as a scope in the client credentials grant, the request will fail. Here's why:

- The 'openid' scope is specific to OpenID Connect (OIDC), which is an identity layer on top of OAuth 2.0.
- The client credentials grant is designed for machine-to-machine communication where there's no user involved.
- OIDC scopes like 'openid', 'profile', or 'email' are meant for obtaining information about a user.
- In a client credentials flow, there's no user context, so these OIDC scopes are not applicable.

If you include 'openid' in your scope request for a client credentials grant, you'll typically receive an error response from the authorization server indicating that the scope is not valid for this grant type.

# User Authentication Flow with Authorization Code Grant

This section demonstrates the OAuth 2.0 Authorization Code flow, which is used for user authentication in web applications.

## Flow Diagram

```mermaid
sequenceDiagram
    participant User
    participant WebApp as Web App (localhost:8080)
    participant Okta as Okta Authorization Server
    participant FakeBookAPI as FakeBook API Resource Server

    User->>WebApp: 1. Initiates login
    WebApp->>Okta: 2. Redirects for authentication
    Okta->>User: 3. Presents login page
    User->>Okta: 4. Enters credentials
    Okta->>WebApp: 5. Redirects with authorization code
    WebApp->>Okta: 6. Exchanges code for access token
    Note right of WebApp: Simulated in Postman
    Okta->>WebApp: 7. Returns access token
    WebApp->>FakeBookAPI: 8. Requests resource with access token
    FakeBookAPI->>WebApp: 9. Returns requested resource
    WebApp->>User: 10. Displays data
```

## Flow Description

1. The user initiates the login process on the web application running on `http://localhost:8080`.
2. The web app redirects the user to Okta for authentication.
3. Okta presents a login page to the user.
4. The user enters their credentials on the Okta login page.
5. Upon successful authentication, Okta redirects back to the web app with an authorization code.
6. The web app exchanges this authorization code for an access token (This step is simulated using Postman in our setup).
7. Okta returns an access token to the web app.
8. The web app uses this access token to request resources from the FakeBook API resource server.
9. The FakeBook API validates the token and returns the requested resources.
10. The web app displays the retrieved data to the user.

This flow ensures secure user authentication and authorization before allowing access to protected resources in the FakeBook API.

## Okta Setup

1. Log in to your Okta Developer Console.

2. Navigate to "Applications" > "Create App Integration".

3. Select "OIDC - OpenID Connect" as the sign-on method and "Web Application" as the application type.

4. Click "Next".

5. Configure the app integration:
   - App integration name: FakebookAuthCodeClient
   - Grant types: Check "Authorization Code" and "Refresh Token"
   - Sign-in redirect URIs: http://localhost:7001
   - Sign-out redirect URIs: http://localhost:7001
   - Controlled access: Allow everyone in your organization to access

6. Click "Save" to create the application.

7. Note down the following credentials (you'll need these for the next steps):
   - Client ID
   - Client Secret

8. Under the "Assignments" tab, ensure that the appropriate users or groups are assigned to the application.

## Authorization Code Flow Steps

After setting up your Okta application, follow these steps to complete the Authorization Code flow:

### STEP 4: Construct an Authorization URL

Construct a URL to send to the Okta Authorization Server:

- Identify your authorize endpoint in your Okta application settings
- Use the following scopes: "openid profile email fakebookapi.read offline_access"

URL Format:
```
https://{YOUR_OKTA_DOMAIN}/oauth2/default/v1/authorize?response_type=code&client_id={YOUR_CLIENT_ID}&state=state123&redirect_uri={YOUR_REDIRECT_URI}&scope={SCOPES}&nonce=test123
```

Replace the placeholders:
- {YOUR_OKTA_DOMAIN}: Your Okta domain (e.g., dev-2148273.okta.com)
- {YOUR_CLIENT_ID}: The client ID of your Okta application
- {YOUR_REDIRECT_URI}: Your configured redirect URI (e.g., http://localhost:7001/callback)
- {SCOPES}: openid profile email fakebookapi.read offline_access

### STEP 5: Run a Local Web Server

Start a local web server to capture the Authorization Code:

```
python -m http.server 7001
```

Note: This step is optional if you've already set up a web server in previous steps.

### STEP 6: Send an Authorization Request

1. Open the constructed URL (from Step 4) in your web browser.
2. Log in using your Okta credentials.
3. After successful authentication, you'll be redirected to your redirect URI.
4. Capture the Authorization Code from:
   - The web server output console, or
   - The browser's address bar in the redirect URL

### STEP 7: Exchange the Authorization Code for Tokens

Construct a token request to exchange the Authorization Code for an access token:

- Use the token endpoint from your Okta application settings
- Use the grant type "authorization_code"
- Include the Authorization Code obtained in Step 6

We'll use Postman to make this request in the next section.

---

These steps demonstrate the core flow of the Authorization Code grant. In a production environment, these steps would typically be handled automatically by your web application.
