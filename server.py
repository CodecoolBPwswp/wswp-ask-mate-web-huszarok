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


@app.route('/question/<int:question_id>/new-answer')
def answer_question(question_id):
    get_question = data_manager.sort_questions_by_date('submission_time', True)
    dict_question = data_manager.from_dict_to_variable(get_question, 'id', question_id)
    list_of_answers = data_manager.get_answers_from_file()
    if request.method == 'GET':
        return render_template('form.html', form_type=3, question_id=question_id,
                               get_question=dict_question, answer_data=list_of_answers)
    if request.method == 'POST':
        return redirect('/question/' + str(question_id))


@app.route('/question/<int:question_id>')
def display_questions(question_id):
    questions = data_manager.sort_questions_by_date('submission_time', True)
    dict_question = data_manager.from_dict_to_variable(questions,'id', question_id)

    answers_of_question = []
    answers = data_manager.sort_answer_by_date('submission_time', True)
    for answer_dict in answers:
        if answer_dict['question_id'] == question_id:
            answers_of_question.append(answer_dict)

    return render_template("form.html",
                           form_type=4,
                           id=question_id,
                           question=dict_question,
                           answers=answers_of_question)


@app.route('/answer/<answer_id>/delete', methods=['POST'])
def delete_answer(answer_id):
    pin = request.form.get('id')
    print(pin)
    return redirect('/')
if __name__ == '__main__':
    app.run(
        debug=True,
        port=5000
    )
