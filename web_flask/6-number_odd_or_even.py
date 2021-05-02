#!/usr/bin/python3
"""This module has the minimum script to start running a web app"""

from flask import Flask, render_template

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


@app.route('/python')
@app.route('/python/<text>')
def parrot_py(text='is_cool'):
    return 'Python {}'.format(text.replace('_', ' '))


@app.route('/number/<int:num>')
def num_detect(num):
    return '{} is a number'.format(num)


@app.route('/number_template/<int:num>')
def num_detect_template(num):
    return render_template('5-number.html', num=num)


@app.route('/number_odd_or_even/<int:num>')
def odd_even_template(num):
    if num % 2 == 0:
        state = 'even'
    else:
        state = 'odd'

    return render_template('6-number_odd_or_even.html', num=num, state=state)


if __name__ == "__main__":
    app.run(debug=True)
