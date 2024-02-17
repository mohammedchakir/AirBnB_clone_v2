#!/usr/bin/python3
"""
This script starts a Flask web application with specified routes.
"""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def close(self):
    """Remove the current SQLAlchemy Session after each request"""
    storage.close()


@app.route('/states', strict_slashes=False)
def state():
    """Display a list of all State objects present in DBStorage"""
    states = storage.all(State)
    return render_template('9-states.html', states=states, mode='all')


@app.route('/states/<id>', strict_slashes=False)
def state_by_id(id):
    """Display cities associated with a State"""
    for state in storage.all(State).values():
        if state.id == id:
            return render_template('9-states.html', states=state, mode='id')
    return render_template('9-states.html', states=state, mode='none')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
