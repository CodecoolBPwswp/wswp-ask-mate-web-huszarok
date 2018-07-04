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
    return render_template('list.html',
                           list_of_questions=list_of_questions,
                           len_of_list_of_questions=len_of_list_of_questions)


@app.route('/add-question', methods=['POST', 'GET'])
def route_form_question():
    if request.method == 'GET':
        return render_template('form.html', form_type=1)
    if request.method == 'POST':
        title = request.form['title']
        question = request.form['question']
        question_id = data_manager.append_question_from_server(title, question)
        return redirect('/question/' + str(question_id))


@app.route('/question/<question_id>/new-answer)')
def answer_question():
    return render_template('form.html', form_type=3)


if __name__ == '__main__':
    app.run(
        debug=True,
        port=5000
    )
