#!/usr/bin/python3
"""This module has the minimum script to start running a web app"""

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hbtn():
    return 'Hello HBNB!'
