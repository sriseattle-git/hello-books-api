from os import abort
from app import db
from app.models.genre import Genre
from app.models.book import Book
from flask import Blueprint, jsonify, abort, make_response, request
from app.book_routes import validate_model

genres_bp = Blueprint("genres", __name__, url_prefix="/genres")

@genres_bp.route("", methods=["POST"])
def create_genre():
    request_body = request.get_json()
    new_genre = Genre(name=request_body["name"])
    
    db.session.add(new_genre)
    db.session.commit()

    return make_response(jsonify(f"Genre {new_genre.name} successfully created"), 201)

@genres_bp.route("", methods=["GET"])
def read_all_genres():
    genres = Genre.query.all()

    genres_response = []
    for genre in genres:
        genres_response.append(
            {
                "name": genre.name,
                "id":genre.id
            }
        )
    return jsonify(genres_response)

@genres_bp.route("<genre_id>/books", methods=["POST"])
def create_book_by_genre(genre_id):
    genre = validate_model(Genre, genre_id)

    request_body = request.get_json()
    new_book = Book.from_dict(request_body)
    new_book.author_id = request_body["author_id"]
    new_book.genres = [genre]

    db.session.add(new_book)
    db.session.commit()

    return make_response(jsonify(f"Book {new_book.title} by {new_book.author.name} successfully created"), 201)

@genres_bp.route("<genre_id>/books/<book_id>", methods=["PATCH"])
def update_book_genre(genre_id, book_id):
    genre = validate_model(Genre, genre_id)
    book = validate_model(Book, book_id)

    book.genres = [genre]

    db.session.commit()

    return make_response(jsonify(f"Book {book.title} by {book.author.name} successfully mapped to {genre.name}"), 200)

@genres_bp.route("<genre_id>/books", methods=["GET"])
def read_all_books_by_genre(genre_id):
    genre = validate_model(Genre, genre_id)

    books_response = []
    for book in genre.books:
        books_response.append(book.to_dict())
        
    return jsonify(books_response)