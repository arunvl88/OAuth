from flask import Flask, jsonify, request, make_response
from flask_restful import Api, Resource
from functools import wraps
from jwt import PyJWKClient, decode as jwt_decode, exceptions as jwt_exceptions

app = Flask(__name__)
api = Api(app)

# Hardcoded JWKS URI from Okta
OKTA_JWKS_URI = 'https://dev-45134456.okta.com/oauth2/default/v1/keys'
jwks_client = PyJWKClient(OKTA_JWKS_URI)

class FakeBook:
    def __init__(self, id, title, author, cost, num_pages):
        self.id = id
        self.title = title
        self.author = author
        self.cost = cost
        self.num_pages = num_pages

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "cost": self.cost,
            "num_pages": self.num_pages
        }

books = [
    FakeBook(1, "And Then There Were None", "Agatha Christie", 7.99, 300),
    FakeBook(2, "A Study in Scarlet", "Arthur Conan Doyle", 7.99, 108),
    FakeBook(3, "The Day of the Jackal", "Frederick Forsyth", 9.99, 464),
    FakeBook(4, "The Wisdom of Father Brown", "G.K. Chesterton", 7.99, 136),
    FakeBook(5, "The Poet", "Michael Connelly", 15.90, 528)
]

def verify_jwt(token):
    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        decoded_token = jwt_decode(
            token, 
            signing_key.key, 
            algorithms=["RS256"], 
            audience='api://default'
        )
        return decoded_token
    except jwt_exceptions.ExpiredSignatureError:
        return {"message": "Token has expired"}, 401
    except jwt_exceptions.InvalidTokenError:
        return {"message": "Invalid token"}, 401

def require_scope(required_scope):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get('Authorization', None)
            if not auth_header:
                return make_response(jsonify({"message": "Missing Authorization Header"}), 401)
            
            token = auth_header.split()[1]
            claims = verify_jwt(token)
            
            if isinstance(claims, tuple):
                # claims is already an error response
                return make_response(jsonify(claims[0]), claims[1])
            
            if required_scope not in claims.get('scp', []):
                return make_response(jsonify({"message": f"{required_scope} scope is required"}), 403)
            
            return fn(*args, **kwargs)
        return wrapper
    return decorator

class BookList(Resource):
    @require_scope('fakebookapi.read')
    def get(self):
        return jsonify([book.to_dict() for book in books])

    @require_scope('fakebookapi.admin')
    def post(self):
        data = request.get_json()
        new_book = FakeBook(
            id=len(books) + 1,
            title=data['title'],
            author=data['author'],
            cost=data['cost'],
            num_pages=data['num_pages']
        )
        books.append(new_book)
        return make_response(jsonify(new_book.to_dict()), 201)

class Book(Resource):
    @require_scope('fakebookapi.read')
    def get(self, book_id):
        book = next((book for book in books if book.id == book_id), None)
        if book:
            return jsonify(book.to_dict())
        return jsonify({"message": "Book not found"}), 404

api.add_resource(BookList, '/books')
api.add_resource(Book, '/books/<int:book_id>')

if __name__ == '__main__':
    app.run(debug=True)
