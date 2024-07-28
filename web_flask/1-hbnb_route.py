#!/usr/bin/python3
"""
Flask web application that displays "Hello HBNB!" at the root URL,
and "HBNB" at /hbnb url.
"""

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
