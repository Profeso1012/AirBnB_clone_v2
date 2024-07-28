#!/usr/bin/python3
"""
A Flask web application with multiple routes and templates.
"""

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """Route that returns a simple greeting."""
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Route that returns 'HBNB'."""
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c_is_fun(text):
    """Route that returns 'C ' followed by the value of the text variable,
    replacing underscores with spaces."""
    return f"C {text.replace('_', ' ')}"


@app.route('/python/', defaults={'text': 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_is_cool(text):
    """Route that returns 'Python ' followed by the value of the text variable,
    replacing underscores with spaces."""
    return f"Python {text.replace('_', ' ')}"


@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    """Route that returns 'n is a number' only if n is an integer."""
    return f"{n} is a number"


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    """Route that returns a HTML page only if n is an integer,
    displaying 'Number: n'."""
    return render_template('number.html', n=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def number_odd_or_even(n):
    """Route that returns a HTML page only if n is an integer,
    displaying 'Number: n is even|odd'."""
    parity = "even" if n % 2 == 0 else "odd"
    return render_template('number_odd_or_even.html', n=n, parity=parity)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
