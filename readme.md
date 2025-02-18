# Book Library Management System

This is a Flask-based web application for managing a library of books and authors. It allows users to add, search, and delete books and authors while displaying book covers fetched using the Open Library Covers API.

## Features
- Add authors with birth and death dates.
- Add books with title, ISBN, publication year, and associated author.
- Search books by title or author name.
- Sort books alphabetically by title or author.
- Display book covers using ISBN (via Open Library API).
- Delete books and authors (deleting an author removes all associated books).

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/prismspecs/book-alchemy-sql.git
cd book-alchemy-sql
```

### 2. Create a Virtual Environment and Install Dependencies
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Initialize the Database
```bash
flask shell
>>> from data_models import db
>>> db.create_all()
>>> exit()
```

### 4. Run the Flask Application
```bash
flask run
```

The application will be available at: [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Configuration
Modify `app.py` to update database paths or change Flask settings as needed.

## API Integration
Book covers are fetched dynamically using the Open Library Covers API:
```
https://covers.openlibrary.org/b/isbn/ISBN_HERE-M.jpg
```
If no cover is available, a placeholder image (`static/placeholder.jpg`) is displayed.

## File Structure
```
/book-alchemy-sql
├── static/
│   ├── style.css
│   ├── placeholder.jpg
├── templates/
│   ├── home.html
│   ├── add_author.html
│   ├── add_book.html
├── app.py
├── data_models.py
├── requirements.txt
├── README.md
```

## Dependencies
- Flask
- Flask-SQLAlchemy

## To-Do
- Implement user authentication
- Add book editing functionality
- Improve UI styling

## License
This project is licensed under the MIT License.

## Contributions
Feel free to submit pull requests or open issues for feature suggestions.

---

Enjoy managing your library! 📚

