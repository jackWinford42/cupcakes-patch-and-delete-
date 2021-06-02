"""Flask app for Cupcakes"""
from flask import Flask, request, jsonify, render_template
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "thisIsSecret"
debug = DebugToolbarExtension(app)

def serialize_cupcake(cupcake):
    """Serialize a cupcake SQLAlchemy object to a dictionary."""

    return {
        "id": cupcake.id,
        "flavor": cupcake.flavor,
        "size": cupcake.size,
        "rating": cupcake.rating,
        "image": cupcake.image
    }

@app.route('/api/cupcakes')
def get_cupcake_data():
    """Return JSON for the individual cupcakes in the kupcakes table"""

    cupcakes = Cupcake.query.all()
    serialized = [serialize_cupcake(c) for c in cupcakes]

    return jsonify(cupcakes=serialized)

@app.route("/api/cupcakes/<cupcake_id>")
def list_single_cupcake(cupcake_id):
    """Return the JSON representation of a single cupcake object"""

    cupcake = Cupcake.query.get(cupcake_id)
    serialized = serialize_cupcake(cupcake)

    return jsonify(cupcake=serialized)

@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    """Create cupcake from form data & return it.

    Returns JSON {'cupcake': {id, flavor, size, rating, image}}
    """

    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json["image"] or None

    new_cupcake = Cupcake(flavor=flavor,
                        size=size,
                        rating=rating,
                        image=image)

    db.session.add(new_cupcake)
    db.session.commit()

    serialized = serialize_cupcake(new_cupcake)

    # Return w/status code 201 --- return tuple (json, status)
    return ( jsonify(cupcake=serialized), 201 )

@app.route("/api/cupcakes/<cupcake_id>", methods=["PATCH"])
def update_cupcake(cupcake_id):
    """Update a cupcake with the id passed in the url and data from the 
    body of the request.

    Returns JSON {'cupcake': {id, flavor, size, rating, image}}
    """

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = request.json["flavor"]
    cupcake.size = request.json["size"]
    cupcake.rating = request.json["rating"]
    cupcake.image = request.json["image"]

    db.session.add(cupcake)
    db.session.commit()

    serialized = serialize_cupcake(cupcake)

    return jsonify(cupcake=serialized)

@app.route("/api/cupcakes/<cupcake_id>", methods=["DELETE"])
def delete_cupcake(cupcake_id):
    """Delete a cupcake with the id passed in the url

    Returns JSON {message: "Deleted"}
    """

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify({"message": "Deleted"})

@app.route("/")
def display_home():
    """display the home page with list of cupcakes and a form"""

    return render_template("home.html")
