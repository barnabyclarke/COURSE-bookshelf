from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)


with app.app_context():
    db.create_all()


def lists():
    all_books = []
    books = db.session.execute(db.select(Books).order_by(Books.id)).scalars()
    for obj in books:
        all_books.append(obj)
    return all_books


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        addition = Books(
            title=request.form['book_name'],
            author=request.form['book_author'],
            rating=request.form['book_rating']
        )
        db.session.add(addition)
        db.session.commit()
    return render_template('index.html', all_books=lists())


@app.route("/add")
def add():
    return render_template('add.html')


@app.route("/edit/<book_id>", methods=['GET', 'POST'])
def edit(book_id):
    if request.method == 'GET':
        book = Books.query.get(book_id)
        return render_template('edit.html', book_edit=book)
    else:
        book_to_update = Books.query.get(book_id)
        book_to_update.rating = request.form['book_rating']
        db.session.commit()
        return render_template('index.html', all_books=lists())


@app.route("/delete/<book_id>")
def delete(book_id):
    book_to_delete = Books.query.get(book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
