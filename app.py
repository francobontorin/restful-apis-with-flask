from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Book

# Connect to Database and create database session
engine = create_engine('sqlite:///books-collection.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

"""
api functions
"""
from flask import jsonify


def get_books():
    books = session.query(Book).all()
    return jsonify(vaccines=[b.serialize for b in books])


def get_book(book_id):
    books = session.query(Book).filter_by(id=book_id).one()
    return jsonify(vaccines=books.serialize)


def makeANewBook(vaccine, lab, quantity, orderby):
    addedbook = Book(vaccine=vaccine, lab=lab, quantity=quantity, orderby=orderby)
    session.add(addedbook)
    session.commit()
    return jsonify(vaccines=addedbook.serialize)


def updateBook(id, vaccine, lab, quantity, orderby):
    updatedBook = session.query(Book).filter_by(id=id).one()
    if not vaccine:
        updatedBook.vaccine = vaccine
    if not lab:
        updatedBook.lab = lab
    if not quantity:
        updatedBook.quantity = quantity
    if not orderby:
        updatedBook.orderby = orderby
    session.add(updatedBook)
    session.commit()
    return 'Updated a Book with id %s' % id


def deleteABook(id):
    bookToDelete = session.query(Book).filter_by(id=id).one()
    session.delete(bookToDelete)
    session.commit()
    return 'Removed Book with id %s' % id


@app.route('/')
@app.route('/vaccines', methods=['GET', 'POST'])
def booksFunction():
    if request.method == 'GET':
        return get_books()
    elif request.method == 'POST':
        vaccine = request.args.get('vaccine', '')
        lab = request.args.get('lab', '')
        quantity = request.args.get('quantity', '')
        orderby = request.args.get('orderby', '')
        return makeANewBook(vaccine, lab, quantity, orderby)


@app.route('/vaccines/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def bookFunctionId(id):
    if request.method == 'GET':
        return get_book(id)

    elif request.method == 'PUT':
        vaccine = request.args.get('vaccine', '')
        lab = request.args.get('lab', '')
        quantity = request.args.get('quantity', '')
        orderby = request.args.get('orderby', '')
        return updateBook(id, vaccine, lab, quantity, orderby)

    elif request.method == 'DELETE':
        return deleteABook(id)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=80)
