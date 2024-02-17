#!/usr/bin/python3
"""
This script starts a Flask web application with specified routes.
"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City

app = Flask(__name__)


@app.teardown_appcontext
def teardown_session(self):
    """Remove the current SQLAlchemy Session after each request"""
    storage.close()


@app.route('/states', strict_slashes=False)
def display_states():
    """Display a list of all State objects present in DBStorage"""
    states = storage.all(State)
    return render_template('9-states.html', states=states)


@app.route('/states/<id>', strict_slashes=False)
def display_state_cities(id):
    """Display cities associated with a State"""
    state = storage.get(State, id)
    if state:
        return render_template('9-states_by_id.html', state=state)
    else:
        return render_template('9-not_found.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
