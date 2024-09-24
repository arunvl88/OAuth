# FakeBook API

## Introduction

FakeBook API is a Flask-based RESTful API that demonstrates OAuth 2.0 integration with Okta for authentication and authorization. This project showcases how to implement secure, scope-based access control for API endpoints using JSON Web Tokens (JWTs) issued by Okta.

The API provides endpoints for managing a collection of books, with different access levels based on OAuth scopes:
- Reading book information requires the 'fakebookapi.read' scope
- Adding new books requires the 'fakebookapi.admin' scope

This setup mimics real-world scenarios where different API operations require different levels of access.

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

## Security Considerations

- Always use HTTPS in production.
- Keep your Okta credentials and JWKS URI confidential.
- Regularly update dependencies to patch any security vulnerabilities.

## Contributing

Contributions to improve the project are welcome. Please follow the standard fork-and-pull request workflow.

## License

[Specify your license here]# OAuth
Understanding OAuth through a project
