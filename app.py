from flask import Flask, render_template, request, redirect, url_for, flash
from data_models import db, Author, Book
from sqlalchemy import or_
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/grayson/workbench/masterschool/book-alchemy/data/library.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Initialize database
db.init_app(app)

# Create database tables if they don't exist
with app.app_context():
    db.create_all()

# --------------------------
# Routes
# --------------------------

@app.route('/', methods=['GET'])
def home():
    try:
        search_query = request.args.get('search', '').strip()
        sort_by = request.args.get('sort_by', 'title')

        # Start with base query
        books_query = Book.query.join(Author)

        # Apply search filter
        if search_query:
            books_query = books_query.filter(or_(
                Book.title.ilike(f'%{search_query}%'),
                Author.name.ilike(f'%{search_query}%')
            ))

        # Apply sorting
        if sort_by == 'author':
            books = books_query.order_by(Author.name).all()
        else:
            books = books_query.order_by(Book.title).all()

        return render_template('home.html',
                             books=books,
                             query=search_query,
                             sort_by=sort_by)

    except Exception as e:
        print(f"Error: {e}")
        flash('Error accessing database. Please try again.', 'error')
        return redirect(url_for('home'))

        

@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    try:
        if request.method == 'POST':
            # Convert date strings to date objects
            birth_date_str = request.form['birth_date']
            date_of_death_str = request.form['date_of_death']

            birth_date = None
            date_of_death = None

            if birth_date_str:
                birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
            if date_of_death_str:
                date_of_death = datetime.strptime(date_of_death_str, '%Y-%m-%d').date()

            new_author = Author(
                name=request.form['name'],
                birth_date=birth_date,
                date_of_death=date_of_death
            )

            db.session.add(new_author)
            db.session.commit()
            flash('Author added successfully!', 'success')
            return redirect(url_for('add_author'))

        return render_template('add_author.html')

    except ValueError as e:
        db.session.rollback()
        flash(f'Invalid date format: {str(e)}. Please use YYYY-MM-DD format.', 'error')
        return redirect(url_for('add_author'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error adding author: {str(e)}', 'error')
        return redirect(url_for('add_author'))


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    try:
        authors = Author.query.order_by(Author.name).all()

        if request.method == 'POST':
            # Create new book from form data
            new_book = Book(
                title=request.form['title'],
                isbn=request.form['isbn'],
                publication_year=request.form['publication_year'] or None,
                author_id=request.form['author_id']
            )
            db.session.add(new_book)
            db.session.commit()
            flash('Book added successfully!', 'success')
            return redirect(url_for('add_book'))

        return render_template('add_book.html', authors=authors)

    except Exception as e:
        db.session.rollback()
        flash(f'Error adding book: {str(e)}', 'error')
        return redirect(url_for('add_book'))


@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    try:
        book = Book.query.get_or_404(book_id)
        author = book.author

        db.session.delete(book)
        db.session.commit()

        # Delete author if no books remain
        if not author.books:
            db.session.delete(author)
            db.session.commit()

        flash(f'Book "{book.title}" deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting book. Please try again.', 'error')

    return redirect(url_for('home'))


@app.route('/author/<int:author_id>/delete', methods=['POST'])
def delete_author(author_id):
    try:
        author = Author.query.get_or_404(author_id)
        author_name = author.name

        db.session.delete(author)
        db.session.commit()

        flash(f'Author "{author_name}" and all associated books deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting author: {str(e)}', 'error')

    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)