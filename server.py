'''Flask stuff (server, routes, request handling, session, etc.)
This layer should consist of logic that is hardly related to Flask.
(with other words: this should be the only file importing from flask)'''

from flask import Flask, render_template, redirect, request
import data_manager


app = Flask(__name__)


@app.route('/')
@app.route('/list')
def list_questions():
    list_of_questions = data_manager.get_questions_from_file()
    len_of_list_of_questions = len(list_of_questions)
    return render_template('list.html', list_of_questions=list_of_questions, len_of_list_of_questions=len_of_list_of_questions)


if __name__ == '__main__':
    app.run(
        debug=True,  # as in the tutorial --> to ask!!
        port=5000  # Set port
    )
