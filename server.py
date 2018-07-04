'''Flask stuff (server, routes, request handling, session, etc.)
This layer should consist of logic that is hardly related to Flask.
(with other words: this should be the only file importing from flask)'''

from flask import Flask, render_template, redirect, request
import data_manager


app = Flask(__name__)


@app.route('/')
@app.route('/list')
def list_questions():
    sortby = request.args.get('sortby','submission_time,1')
    sortby = sortby.split(',')
    list_of_questions = data_manager.sort_questions_by_date(sortby[0],bool(int(sortby[1])))
    len_of_list_of_questions = len(list_of_questions)
    return render_template('list.html',
                           list_of_questions=list_of_questions,
                           len_of_list_of_questions=len_of_list_of_questions)


@app.route('/add-question', methods=['POST', 'GET'])
def add_question():
    if request.method == 'GET':
        return render_template('form.html', form_type=1)
    if request.method == 'POST':
        title = request.form['title']
        message = request.form['message']
        question_id = data_manager.append_question_from_server(title, message)
        return redirect('/question/' + str(question_id))


@app.route('/question/<question_id>/edit', methods=['POST', 'GET'])
def edit_question(question_id):
    list_of_questions = data_manager.get_questions_from_file()
    for question in list_of_questions:
        if question['id'] == question_id:
            question_data = question
    if request.method == 'GET':
        return render_template('form.html', form_type=2, question_data=question_data)
    if request.method == 'POST':
        title = request.form['title']
        message = request.form['message']
        data_manager.update_question_from_server(title, message, question_data)
        return redirect('/question/' + str(question_id))


@app.route('/question/<question_id>/new-answer)')
def answer_question(question_id):
    return render_template('form.html', form_type=3)


@app.route('/question/<question_id>')
def display_questions(question_id):
    answer = []
    get_question = data_manager.get_questions_from_file()
    get_answer = data_manager.get_answers_from_file()
    for dict_items in get_question:
        for key, value in dict_items.items():
            if dict_items['id'] == question_id:
                question = dict_items
    for answer_items in get_answer:
        for key, value in answer_items.items():
            if answer_items['question_id'] == question_id:
                answer.append(answer_items)
    return render_template("form.html", form_type=4,
                           id=question_id, get_question=question, get_answer=answer)


if __name__ == '__main__':
    app.run(
        debug=True,
        port=5000
    )
