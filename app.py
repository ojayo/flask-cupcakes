"""Flask app for Cupcakes"""
from flask import Flask, request, jsonify
from models import db, connect_db, Cupcake
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'bigsecret'
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


def serialize_cupcake(cupcake):
    """ Serialize a cupcake -- SQLAlchemy obj to dictionary """

    return {
        "id": cupcake.id,
        "flavor": cupcake.flavor,
        "size": cupcake.size,
        "rating": cupcake.rating,
        "image": cupcake.image,
    }


@app.route('/api/cupcakes')
def get_all_cupcakes():
    """ show all the cupcakes """

    cupcakes = Cupcake.query.all()
    serialized = [serialize_cupcake(c) for c in cupcakes]

    return jsonify(cupcakes=serialized)


@app.route('/api/cupcakes/<cupcake_id>')
def get_single_cupcake(cupcake_id):
    """ Show data for a single cupcake """

    cupcake = Cupcake.query.get(cupcake_id)
    serialized = serialize_cupcake(cupcake)

    return jsonify(cupcake=serialized)


@app.route('/api/cupcakes', methods=['POST'])
def create_new_cupcake():
    """ Create a new cupcake instance
    returns JSON {'cupcake': {id, flavor, size, rating, image }} """

    flavor = request.json['flavor']
    size = request.json['size']
    rating = request.json['rating']
    image = request.json.get('image') or None 
    # for image, use json.get just in case the image doesn't exist

    new_cupcake = Cupcake(flavor=flavor,
                          size=size,
                          rating=rating,
                          image=image)

    db.session.add(new_cupcake)
    db.session.commit()

    serialized = serialize_cupcake(new_cupcake)

    return (jsonify(cupcake=serialized), 201)


@app.route('/api/cupcakes/<cupcake_id>', methods=['PATCH'])
def update_cupcake_data(cupcake_id):
    """ Update cupcake with the data passed in"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = request.json.get('flavor') or cupcake.flavor
    cupcake.size = request.json.get('size') or cupcake.size
    cupcake.rating = request.json.get('rating') or cupcake.rating
    cupcake.image = request.json.get('image') or cupcake.image

    db.session.add(cupcake)
    db.session.commit()

    serialized = serialize_cupcake(cupcake)

    return (jsonify(cupcake=serialized), 200)


@app.route('/api/cupcakes/<cupcake_id>', methods=['DELETE'])
def delete_cupcake(cupcake_id):
    """ Delete the cupcake """

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return {"Cupcake": "Deleted"}