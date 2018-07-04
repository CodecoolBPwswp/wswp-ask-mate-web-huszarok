'''Flask stuff (server, routes, request handling, session, etc.)
This layer should consist of logic that is hardly related to Flask.
(with other words: this should be the only file importing from flask)'''

from flask import Flask, render_template, redirect, request
import data_manager


app = Flask(__name__)


@app.route('/')
@app.route('/list')
def list_questions():
    list_of_questions = data_manager.sort_questions_by_date()
    len_of_list_of_questions = len(list_of_questions)
    return render_template('list.html', list_of_questions=list_of_questions, len_of_list_of_questions=len_of_list_of_questions)


@app.route('/add-question')
def route_form_question():
    return render_template('form.html', form_type=1)


@app.route('/question/<question_id>')
def display_questions(question_id):
    get_question = data_manager.get_questions_from_file()
    get_answer = data_manager.get_answers_from_file()

    return render_template("form.html", form_type=4,
                           id=question_id, get_question=get_question, get_answer=get_answer)


if __name__ == '__main__':
    app.run(
        debug=True,  # as in the tutorial --> to ask!!
        port=5000  # Set port
    )
