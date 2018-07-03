'''Flask stuff (server, routes, request handling, session, etc.)
This layer should consist of logic that is hardly related to Flask.
(with other words: this should be the only file importing from flask)'''
from flask import Flask, render_template, redirect, request

app = Flask(__name__)


@app.route('/add-question)')
def route_form_question():
    return render_template('form.html', form_type=1)


if __name__ == '__main__':
    app.secret_key = '42'
    app.run(
        host="0.0.0.0",
        debug=True,
        port=5000