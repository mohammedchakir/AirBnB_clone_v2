#!/usr/bin/python3
"""
This module starts a Flask web application.
"""

from flask import Flask
from urllib.parse import unquote

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


@app.route('/c/<text>', strict_slashes=False)
def display_c_text(text):
    """
    Display "C " followed by the value of the text variable.
    """
    text = unquote(text)
    text = text.replace("_", " ")
    return 'C {}'.format(text)


@app.route('/python/', defaults={'text': 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def display_python_text(text):
    """
    Display "Python " followed by the value of the text variable.
    """
    text = unquote(text.replace("_", " "))
    return 'Python {}'.format(text)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
