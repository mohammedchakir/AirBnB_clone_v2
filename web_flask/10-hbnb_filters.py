#!/usr/bin/python3
"""
This script starts a Flask web application with specified routes.
"""

from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity

app = Flask(__name__)


@app.teardown_appcontext
def teardown_session(exception):
    """Remove the current SQLAlchemy Session after each request"""
    storage.close()


@app.route('/hbnb_filters', strict_slashes=False)
def display_hbnb_filters():
    """Display a HTML page with Airbnb filters"""
    states = storage.all(State).values()
    sorted_states = sorted(states, key=lambda x: x.name)
    cities = storage.all(City).values()
    sorted_cities = sorted(cities, key=lambda x: x.name)
    amenities = storage.all(Amenity).values()
    sorted_amenities = sorted(amenities, key=lambda x: x.name)
    return render_template('10-hbnb_filters.html', states=sorted_states,
                           cities=sorted_cities, amenities=sorted_amenities)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
