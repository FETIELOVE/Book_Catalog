from flask import Flask, render_template, request, redirect, url_for
from models.database import BookDatabase
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
book_db = BookDatabase()


SWAGGER_URL = '/api/docs'
API_URL = '/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Book Catalog API"}
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


# Ensure there's no duplicate 'index' route
@app.route('/')
def index():
    books = book_db.get_all_books()
    return render_template('index.html', books=books)


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        new_book = {
            'title': request.form['title'],
            'author': request.form['author'],
            'published_year': request.form['published_year'],
            'genre': request.form['genre']
        }
        book_db.add_book(new_book)
        return redirect(url_for('index'))
    return render_template('add_book.html')


@app.route('/search_books')
def search_books():
    query = request.args.get('query', '')
    books = book_db.collection.find({'$or': [
        {'title': {'$regex': query, '$options': 'i'}},
        {'author': {'$regex': query, '$options': 'i'}},
        {'genre': {'$regex': query, '$options': 'i'}}
    ]})
    return render_template('index.html', books=books)


@app.route('/view_book/<book_id>')
def view_book(book_id):
    book = book_db.get_book_by_id(book_id)
    return render_template('view_book.html', book=book)


@app.route('/edit_book/<book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    book = book_db.get_book_by_id(book_id)
    if request.method == 'POST':
        updated_book = {
            'title': request.form['title'],
            'author': request.form['author'],
            'published_year': request.form['published_year'],
            'genre': request.form['genre']
        }
        book_db.update_book(book_id, updated_book)
        return redirect(url_for('index'))
    return render_template('edit_book.html', book=book)


@app.route('/api/docs')
def api_docs():
    return render_template('api_docs.html')


if __name__ == '__main__':
    app.run(debug=True)
