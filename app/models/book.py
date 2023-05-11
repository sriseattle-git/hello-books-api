from app import db
from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import declarative_base, relationship

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    author_id = Column(Integer, ForeignKey("author.id"))
    author = relationship("Author", back_populates="books")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description
        }
    
    @classmethod 
    def from_dict(cls, book_dict):
        new_book = cls(title=book_dict["title"], 
                        description=book_dict["description"])
        return new_book
