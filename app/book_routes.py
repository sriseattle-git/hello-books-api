from os import abort
from app import db
from app.models.book import Book
from flask import Blueprint, jsonify, abort, make_response, request

books_bp = Blueprint("books", __name__, url_prefix="/books")

@books_bp.route("", methods=["GET", "POST"])
def handle_books():
    if request.method == "GET":
        # Retrieve query params, if any
        query_title = request.args.get("title")
        if query_title:
            # Found query param, use it to filter results
            books = Book.query.filter_by(title=query_title)
            # Check if any records returned on query
            if books.count() == 0:
                return make_response({"message":f"book {query_title} not found"}, 200)
        else:
            books = Book.query.all()

        books_response = []
        for book in books:
            books_response.append(book.to_dict())
        
        return jsonify(books_response)
    elif request.method == "POST":
        request_body = request.get_json()
        new_book = Book.from_dict(request_body)
    
        db.session.add(new_book)
        db.session.commit()

        return make_response(jsonify(f"Book {new_book.title} successfully created"), 201)

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)
    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))

    return model

@books_bp.route("/<book_id>", methods=["GET", "PUT"])
def handle_one_book(book_id):
    book = validate_model(Book, book_id)

    if request.method == "GET":
        return book.to_dict()
    elif request.method == "PUT":
        request_body = request.get_json()
        book.title = request_body["title"]
        book.description = request_body["description"]

        db.session.commit()

        return make_response(jsonify(f"Book #{book.id} successfully updated"))
    
@books_bp.route("/<book_id>", methods=["DELETE"])
def delete_one_book(book_id):
    book = validate_model(Book, book_id)

    db.session.delete(book)
    db.session.commit()

    return make_response(jsonify(f"Book #{book.id} successfully deleted"))


############## ONLY COMMENTED CODE BELOW #########################

# hello_world_bp = Blueprint("hello_world", __name__)

# @hello_world_bp.route("/hello-world", methods=["GET"])
# def say_hello_world():
#     my_beautiful_response_body = "Hello, World!"
#     return my_beautiful_response_body

# @hello_world_bp.route("/hello/JSON", methods=["GET"])
# def say_hello_json():
#     return {
#         "name": "Sri R",
#         "message": "Hiya!",
#         "hobbies": ["Biking", "Reading", "Hking"]
#     }

# @hello_world_bp.route("/broken-endpoint-with-broken-server-code", methods=["GET"])
# def broken_endpoint():
#     response_body = {
#         "name": "Sri R",
#         "message": "Hiya!",
#         "hobbies": ["Biking", "Reading", "Hking"]
#     }
#     new_hobby = "Teaching"
#     response_body["hobbies"].append(new_hobby)
#     return response_body

#class Book:
#    def __init__(self, id, title, description):
#        self.id = id
#        self.title = title
#        self.description = description

#books = [
#    Book(1, "Fictional Book Title", "A fantasy novel set in an imaginary world."),
#    Book(2, "Fictional Book Title", "A fantasy novel set in an imaginary world."),
#    Book(3, "Fictional Book Title", "A fantasy novel set in an imaginary world.")
#] 

# def validate_book(book_id):
#     try:
#         book_id = int(book_id)
#     except:
#         abort(make_response({"message":f"book {book_id} invalid"}, 400))

#     for book in books:
#         if book.id == book_id:
#             return book

#     abort(make_response({"message":f"book {book_id} not found"}, 404))

# @books_bp.route("", methods=["GET"])
# def handle_books():
#     books_response = []
#     for book in books:
#         books_response.append({
#             "id": book.id,
#             "title": book.title,
#             "description": book.description
#         })

#     return jsonify(books_response)

# @books_bp.route("/<book_id>", methods=["GET"])
# def handle_book(book_id):
#     book = validate_book(book_id)

#     return {
#         "id": book.id,
#         "title": book.title,
#         "description": book.description
#     }
