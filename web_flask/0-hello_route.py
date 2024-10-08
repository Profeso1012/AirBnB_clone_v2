#!/usr/bin/python3
"""
A simple Flask web application that displays "Hello HBNB!" at the root URL.
"""

from flask import Flask

app = Flask(__name__)


@app.route('/airbnb-onepage', strict_slashes=False)
def hello_hbnb():
    """Route that returns a simple greeting."""
    return "Hello HBNB!"


if __name__ == "__main__":
    #app.run()
    app.run(host="0.0.0.0", port=5000)
