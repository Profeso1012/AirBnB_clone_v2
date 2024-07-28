#!/usr/bin/python3
"""A Flask web application with multiple routes."""

from flask import Flask

app = Flask(__name__)

@app.route('/', strict_slashes=False)
def hello_hbnb():
    """Route that returns a simple greeting."""
    return "Hello HBNB!"

@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Route that returns a text 'HBNB'"""
    return "HBNB"

@app.route('/c/<text>', strict_slashes=False)
def c_text(text):
    """Route that returns 'C ' followed by the value of the text variable.
    """
    return "C " + text.replace('_', ' ')

@app.route('/python/<text>', strict_slashes=False, defaults={'text': 'cool'})
def python_text(text):
    """Route that display Python followed by the value of the text variable"""
    return "Python" + text.replace('_', ' ')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
