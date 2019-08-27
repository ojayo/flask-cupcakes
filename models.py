""" Models for Cupcake app. """

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Cupcake(db.Model):
    """ The Prototypical Cupcake. """

    __tablename__ = "cupcakes"

    default_img = "https://thestayathomechef.com/wp-content/uploads/2017/12/Most-Amazing-Chocolate-Cupcakes-1-small.jpg"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)

    flavor = db.Column(db.Text, nullable=False)
    size = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    image = db.Column(db.Text, default=default_img)


def connect_db(app):
    db.app = app
    db.init_app(app)