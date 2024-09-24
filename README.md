#OAuth 2.0 Client Credentials Flow

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

# FakeBook API

## Introduction

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

1. **Flask and Flask-RESTful Setup**:
   The application uses Flask as the web framework and Flask-RESTful for creating RESTful APIs.

2. **JWT Verification**:
   Custom JWT verification is implemented using PyJWKClient, which fetches the signing key from Okta's JWKS endpoint.

3. **Scope-based Access Control**:
   The `require_scope` decorator checks for required scopes in the JWT claims.

4. **Book Model and Data**:
   A simple `FakeBook` class represents book objects, with a list of books stored in memory.

5. **API Resources**:
   - `BookList`: Handles GET (list all books) and POST (add a new book) requests.
   - `Book`: Handles GET requests for individual books.

### Key Functions

1. **verify_jwt(token)**:
   Verifies the JWT using Okta's JWKS. It handles token expiration and invalidity.

2. **require_scope(required_scope)**:
   A decorator that checks if the JWT contains the required scope for the operation.

3. **before_request()**:
   Ensures the application remains stateless by disabling session creation.

## API Endpoints

- GET /books: Retrieve all books (requires 'fakebookapi.read' scope)
- POST /books: Add a new book (requires 'fakebookapi.admin' scope)
- GET /books/<id>: Retrieve a specific book (requires 'fakebookapi.read' scope)

## Testing

You can test the API using tools like Postman or curl. Remember to include a valid JWT token in the Authorization header of your requests:

```
Authorization: Bearer <your_jwt_token>
```
**Step 1 and 2:** Get token (JWT) from Okta for a specific scope (for ex: fakebookapi.read)

```json
=============================================================================
STEP 1 : Construct a Token Request for Client credentials
============================================================================

ENDPOINT   => https://dev-45134456.okta.com/oauth2/default/v1/token
HTTP TYPE  => POST

grant_type=client_credentials
client_id=<client_id>
client_secret=<client_secret>
scope= fakebookapi.read
```

```json
=============================================================================
STEP 2 : Send Token Request and extract Token
=============================================================================

=> Use openid as scope and it should fail ( why? )
=> Okta returns JWT access tokens 
=> Dissect token in jwt.io 
=> No ID token and no refresh token
```

<img width="1291" alt="image" src="https://github.com/user-attachments/assets/47782948-46c4-4865-b1da-a0a28f927ce5">


**Step 3 and 4:** Use that token to send a request to the Flask App

```json
=============================================================================
STEP 4 : Send a FakeBookAPI request (Get one Books)
=============================================================================

ENDPOINT   => http://localhost:5000/books/1
HTTP TYPE  => GET 

{Pass Bearer token in header}
```

<img width="1315" alt="image" src="https://github.com/user-attachments/assets/77e4e3af-d813-4182-aaae-aa87c81fe5dc">


Step 5: Create a book. The below fails because the Access token we received earlier is only for [fakebookapi.read](http://fakebookapi.read) scope.  

```json
=============================================================================
STEP 5 : Send a FakeBookAPI request (Create a book)
=============================================================================

ENDPOINT   => http://localhost:8080/books
HTTP TYPE  => POST 

{Pass Bearer token in header}
{Pass JSON in BODY}
```

to summarize:

- To read books (GET /books or GET /books/<id>), the JWT token must have the 'fakebookapi.read' scope.
- To create a new book (POST /books), the JWT token must have the 'fakebookapi.admin' scope.
- If a token doesn't have the required scope, the request will be denied with a 403 error.

In order to fix this we need to get a new token which also contains [fakebookapi.](http://fakebookapi.read)admin scope.

```json
=============================================================================
STEP 1 : Construct a Token Request for Client credentials
============================================================================

ENDPOINT   => https://dev-45134456.okta.com/oauth2/default/v1/token
HTTP TYPE  => POST

grant_type=client_credentials
client_id=<client_id>
client_secret=<client_secret>
scope= fakebookapi.read fakebookapi.admin
```

test




