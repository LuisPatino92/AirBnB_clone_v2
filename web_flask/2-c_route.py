#!/usr/bin/python3
"""This module has the minimum script to start running a web app"""

from flask import Flask

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/')
def hbtn():
    return 'Hello HBNB!'


@app.route('/hbnb')
def hbnb():
    return 'HBNB'


@app.route('/c/<text>')
def parrot(text):
    return 'C {}'.format(text.replace('_', ' '))


if __name__ == "__main__":
    app.run(debug=True)
