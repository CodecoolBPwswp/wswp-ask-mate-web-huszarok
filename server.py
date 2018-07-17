'''Flask stuff (server, routes, request handling, session, etc.)
This layer should consist of logic that is hardly related to Flask.
(with other words: this should be the only file importing from flask)'''

from flask import Flask, render_template, redirect, request
import data_manager


app = Flask(__name__)


@app.route('/')
@app.route('/list')
def list_questions():
    columns = ['id', 'submission_time', 'title', 'view_number', 'vote_number']
    sortby = request.args.get('sortby','submission_time,DESC')
    sortby = sortby.split(',')
    rule = request.url_rule
    if '/list' in rule.rule:
        limit = None
        list_of_questions = data_manager.get_all_data_from_file(columns, 'question', sortby[0], sortby[1], limit)
    else:
        limit = 5
        list_of_questions = data_manager.get_all_data_from_file(columns, 'question', sortby[0], sortby[1], limit)

    len_of_list_of_questions = len(list_of_questions)

    return render_template('list.html',
                           list_of_questions=list_of_questions,
                           len_of_list_of_questions=len_of_list_of_questions)


@app.route('/comments/<int:comment_id>/delete')
def delete_comments(comment_id):
    data_manager.delete_comments('comment', comment_id)
    return redirect('/')


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
    if request.method == 'GET':
        columns = ['title', 'message']
        question_data = data_manager.get_data_by_id(columns, 'question', question_id)
        return render_template('form.html', form_type=2, question_data=question_data)
    if request.method == 'POST':
        title = request.form['title']
        message = request.form['message']
        data_manager.update_data('message', 'question', message, question_id)
        data_manager.update_data('title', 'answer', title, question_id)
        return redirect('/question/' + str(question_id))


@app.route('/question/<int:question_id>/new-answer', methods=['POST', 'GET'])
def answer_question(question_id):
    get_question = data_manager.sort_questions_by_date('submission_time', True)
    dict_question = data_manager.from_dict_to_variable(get_question, 'id', question_id)
    list_of_answers = data_manager.get_answers_from_file()
    if request.method == 'GET':
        return render_template('question_display.html', form_type=3, question_id=question_id,
                               question=dict_question, answer_data=list_of_answers)
    if request.method == 'POST':
        message = request.form['message']
        data_manager.append_answer_from_server(question_id, message)
        return redirect('/question/' + str(question_id))


@app.route('/question/<int:question_id>', methods=['POST', 'GET'])
def display_question(question_id):
    columns_for_questions = ['id', 'submission_time', 'title', 'message', 'view_number', 'vote_number']
    columns_for_answers = ['id', 'submission_time', 'message', 'vote_number', 'question_id']
    question = data_manager.get_data_by_id(columns_for_questions, 'question', question_id)
    limit = None
    answers_of_question = data_manager.get_all_data_from_file(columns_for_answers,
                                                              'answer',
                                                              'submission_time',
                                                              'DESC',
                                                              limit)
    comment = request.form.get('comment')
    data_manager.comment_update(comment, question_id, 'comment')
    return render_template("question_display.html",
                           id=question_id,
                           question=question,
                           answers=answers_of_question)


@app.route('/question/<int:question_id>/new-comment', methods=['POST', 'GET'])
def comment_question(question_id):
    comment=request.form.get('comment')
    data_manager.comment_update(comment, question_id, 'comment')

    return render_template("question_comment.html",
                           question_id=question_id)

@app.route('/question/<int:question_id>/vote-up', methods=['POST', 'GET'])
def vote_up_questions(question_id):
        list_of_questions = data_manager.sort_questions_by_date('submission_time', True)
        for question in list_of_questions:
            if question['id'] == question_id:
                question_data = question
        if request.method == 'POST':
            question_data['vote_number'] += 1
            data_manager.vote(question_data)
        return redirect('/question/' + str(question_id))


@app.route('/question/<int:question_id>/vote-down', methods=['POST', 'GET'])
def vote_down_questions(question_id):
    list_of_questions = data_manager.sort_questions_by_date('submission_time', True)
    for question in list_of_questions:
        if question['id'] == question_id:
            question_data = question
    if request.method == 'POST':
        question_data['vote_number'] -= 1
        data_manager.vote(question_data)
    return redirect('/question/' + str(question_id))


if __name__ == '__main__':
    app.run(
        debug=True,
        port=5000
    )
