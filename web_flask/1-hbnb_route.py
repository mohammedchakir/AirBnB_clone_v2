#!/usr/bin/python3
"""
This module starts a Flask web application.
"""

from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """
    Display "Hello HBNB!" on the root route.
    """
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def display_hbnb():
    """
    Display "HBNB" on the '/hbnb' route.
    """
    return 'HBNB'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
