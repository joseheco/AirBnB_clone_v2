#!/usr/bin/python3
"""Start flask application"""

from flask import Flask
app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_world():
    """Return hello hbnb"""
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """Return hbnb"""
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c_text(text):
    """Returns a string at the c"""
    return "C {:s}".format(text.replace("_", " "))


@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_text(text="is cool"):
    """display messagei is cool"""
    return "Python {:s}".format(text.replace("_", " "))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
