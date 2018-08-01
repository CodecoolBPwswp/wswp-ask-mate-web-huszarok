from flask import Flask, render_template, redirect, request, url_for, session
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
        return render_template('list_all.html',
                               list_of_questions=list_of_questions)
    else:
        limit = 5
        list_of_questions = data_manager.get_all_data_from_file(columns, 'question', sortby[0], sortby[1], limit)
        return render_template('list.html',
                               list_of_questions=list_of_questions)


@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'GET':
        search_phrase = request.args.get('phrase')
        if search_phrase is None:
            return render_template('search.html')
        if search_phrase is not None:
            columns = ['id',
                       'submission_time',
                       'title',
                       'view_number',
                       'vote_number']
            list_of_questions = data_manager.get_data_by_search(columns, 'question', search_phrase)
            len_of_list_of_questions = len(list_of_questions)
            return render_template('search_result.html',
                                   list_of_questions=list_of_questions,
                                   len_of_list_of_questions=len_of_list_of_questions)
    if request.method == 'POST':
        query = request.form['search']
        return redirect('/search?phrase=' + query)


@app.route('/comments/<int:comment_id>/delete', methods=['POST'])
def delete_comments(comment_id):
    columns = ['id', 'question_id', 'answer_id']
    comment = data_manager.get_data_by_id(columns, 'comment', comment_id, 'id')
    columns_for_answer = ['id', 'question_id']
    question = data_manager.get_data_by_id(columns_for_answer, 'answer', comment[0]['answer_id'], 'id')
    data_manager.delete('comment', comment_id, 'id')
    if comment[0]['question_id'] is None:
        return redirect('/question/' + str(question[0]['question_id']))
    else:
        return redirect('/question/' + str(comment[0]['question_id']))


@app.route('/answer/<int:answers_id>/delete', methods=['POST'])
def delete_answers(answers_id):
    columns = ['id', 'question_id']
    answer = data_manager.get_data_by_id(columns, 'answer', answers_id, 'id')
    data_manager.delete('comment', answers_id, 'answer_id')
    data_manager.delete('answer', answers_id, 'id')
    return redirect('/question/' + str(answer[0]['question_id']))


@app.route('/question/<int:question_id>/delete', methods=['POST'])
def delete_questions(question_id):
    data_manager.delete('comment', question_id, 'question_id')
    columns = ['id', 'question_id']
    answers = data_manager.get_data_by_id(columns, 'answer', question_id, 'question_id')
    for answer in answers:
        data_manager.delete('comment', answer['id'], 'answer_id')
    data_manager.delete('answer', question_id, 'question_id')
    data_manager.delete('question_tag', question_id, 'question_id')
    data_manager.delete('question', question_id, 'id')
    return redirect('/')


@app.route('/add-question', methods=['POST', 'GET'])
def add_question():
    if request.method == 'GET':
        return render_template('form.html', form_type=1)
    if request.method == 'POST':
        title = request.form['title']
        message = request.form['message']
        data_manager.add_question(title, message)
        return redirect('/')


@app.route('/question/<question_id>/edit', methods=['POST', 'GET'])
def edit_question(question_id):
    if request.method == 'GET':
        columns = ['id', 'title', 'message']
        question_data = data_manager.get_data_by_id(columns, 'question', question_id, 'id')
        return render_template('form.html', form_type=2, question_data=question_data)
    if request.method == 'POST':
        title = request.form['title']
        message = request.form['message']
        data_manager.update_data('message', 'question', message, question_id)
        data_manager.update_data('title', 'question', title, question_id)
        return redirect('/question/' + question_id)


@app.route('/answer/<answer_id>/edit', methods=["GET", "POST"])
def answer_edit(answer_id):
    columns = ['id', 'message', 'question_id']
    answer = data_manager.get_data_by_id(columns, 'answer', answer_id, 'id')
    if request.method == 'GET':
        return render_template("edit_answer.html", answer=answer)
    if request.method == 'POST':
        message = request.form['message']
        data_manager.update_data('message', 'answer', message, answer_id)
        return redirect('/question/' + str(answer[0]['question_id']))


@app.route('/comments/<comment_id>/edit', methods=['GET', 'POST'])
def edit_comment(comment_id):
    columns = ['id', 'question_id', 'answer_id', 'message']
    comment = data_manager.get_data_by_id(columns, 'comment', comment_id, 'id')
    if request.method == 'GET':
        return render_template('edit_comment.html', comment=comment)
    elif request.method == 'POST':
        message = request.form['message']
        data_manager.update_data('message', 'comment', message, comment_id)
        if comment[0]['question_id'] is None:
            columns_for_answer = ['id', 'question_id']
            question = data_manager.get_data_by_id(columns_for_answer, 'answer', comment[0]['answer_id'], 'id')
            return redirect('/question/' + str(question[0]['question_id']))
        else:
            return redirect('/question/' + str(comment[0]['question_id']))


@app.route('/question/<int:question_id>/new-answer', methods=['POST', 'GET'])
def answer_question(question_id):
    columns_for_questions = ['id', 'submission_time', 'title', 'message', 'view_number', 'vote_number']
    columns_for_answers = ['id', 'submission_time', 'message', 'vote_number', 'question_id']
    question = data_manager.get_data_by_id(columns_for_questions, 'question', question_id, 'id')
    limit = None
    answers_of_question = data_manager.get_all_data_from_file(columns_for_answers,
                                                              'answer',
                                                              'submission_time',
                                                              'DESC',
                                                              limit)
    if request.method == 'GET':
        return render_template("new_answer.html",
                               id=question_id,
                               question=question,
                               answers=answers_of_question)
    elif request.method == 'POST':
        message = request.form.get('message')
        data_manager.answer_question(message, question_id, 'answer')
        return redirect(url_for('display_question', question_id=question_id))


@app.route('/question/<int:question_id>', methods=['POST', 'GET'])
def display_question(question_id):
    comments_of_answers={}
    columns_for_questions = ['id', 'submission_time', 'title', 'message', 'view_number', 'vote_number']
    columns_for_answers = ['id', 'submission_time', 'message', 'vote_number', 'question_id']
    columns_for_comment = ['id', 'question_id', 'answer_id', 'message', 'submission_time', 'edited_count']

    question = data_manager.get_data_by_id(columns_for_questions, 'question', question_id, 'id')
    comments_of_question = data_manager.get_data_by_id(columns_for_comment, 'comment', question_id, 'question_id')
    answers_of_question = data_manager.get_data_by_id(columns_for_answers, 'answer', question_id, 'question_id')
    answer_ids = data_manager.get_id_question_or_answer(question_id)

    for answer_id in answer_ids:
        comments_of_answer = data_manager.get_data_by_id(columns_for_comment, 'comment', answer_id['id'], 'answer_id')
        comments_of_answers[answer_id['id']] = comments_of_answer
    get_tag = data_manager.get_tags_name(question_id)

    return render_template("question_display.html",
                           id=question_id,
                           question=question,
                           answers=answers_of_question,
                           comments=comments_of_question,
                           comments_of_answers=comments_of_answers,
                           tags=get_tag)


@app.route('/question/<int:question_id>/new-comment', methods=['POST', 'GET'])
def comment_question(question_id):
    columns = ['id']
    question = data_manager.get_data_by_id(columns, 'question', question_id, 'id')
    if request.method == 'GET':
        return render_template("question_comment.html", question_id=question_id)
    if request.method == 'POST':
        comment = request.form.get('comment')
        data_manager.add_comment_to_question(comment, question_id, 'comment')
        return redirect('/question/' + str(question[0]['id']))


@app.route('/question/<int:answer_id>/new-comments', methods=['GET', 'POST'])
def comment_answer(answer_id):
    columns = ['id', 'question_id']
    question = data_manager.get_data_by_id(columns, 'answer', answer_id, 'id')
    if request.method == 'GET':
        return render_template("answer_comment.html", answer_id=answer_id)
    if request.method == 'POST':
        comment = request.form.get('comment_answer')
        data_manager.add_comment_to_answer(comment, answer_id, 'comment')

    return redirect('/question/' + str(question[0]['question_id']))


@app.route('/question/<int:question_id>/vote-up', methods=['POST', 'GET'])
def vote_up_questions(question_id):
    columns = ['id']
    question = data_manager.get_data_by_id(columns, 'question', question_id, 'id')
    if request.method == 'POST':
        data_manager.increment_vote_number('question', question_id)
    return redirect('/question/' + str(question[0]['id']))


@app.route('/answer/<int:answer_id>/vote-up', methods=['POST', 'GET'])
def vote_up_answers(answer_id):
    columns = ['id', 'question_id']
    answer = data_manager.get_data_by_id(columns, 'answer', answer_id, 'id')
    if request.method == 'POST':
        data_manager.increment_vote_number('answer', answer_id)
    return redirect('/question/' + str(answer[0]['question_id']))


@app.route('/question/<int:question_id>/vote-down', methods=['POST', 'GET'])
def vote_down_questions(question_id):
    columns = ['id']
    question = data_manager.get_data_by_id(columns, 'question', question_id, 'id')
    if request.method == 'POST':
        data_manager.decrement_vote_number('question', question_id)
    return redirect('/question/' + str(question[0]['id']))


@app.route('/answer/<int:answer_id>/vote-down', methods=['POST', 'GET'])
def vote_down_answers(answer_id):
    columns = ['id', 'question_id']
    answer = data_manager.get_data_by_id(columns, 'answer', answer_id, 'id')
    if request.method == 'POST':
        data_manager.decrement_vote_number('answer', answer_id)
    return redirect('/question/' + str(answer[0]['question_id']))


@app.route('/question/<int:question_id>/new-tag', methods=['POST', 'GET'])
def add_new_tag(question_id):
    if request.method == 'POST':
        new_tags = request.form.get('tag')
        data_manager.add_tag(question_id, 'tag', new_tags)
    return render_template('tag_question.html', question_id=question_id)


@app.route('/registration', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template('registration.html')
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        plain_text_password = request.form.get('password')
        repeat_password = request.form.get('password-repeat')
        hashed_pw = data_manager.hash_password(plain_text_password)
        verified_pw = data_manager.verify_password(repeat_password, hashed_pw)
        if verified_pw:
            success_state = data_manager.register(username, email, hashed_pw)
            if success_state:
                return redirect('/')
            else:
                success = False
                return render_template('registration.html', success=success)
        else:
            verified = False
            return render_template('registration.html', verified=verified)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['pwd']
        user_data = data_manager.get_user_data(username)
        if not user_data:
            success = False
            return render_template('login.html', success=success)
        else:
            verified_pw = data_manager.verify_password(password, user_data['password'])
            if verified_pw:
                session['username'] = username
                session['user_id'] = user_data['id']
                return redirect('/')
            else:
                success = False
                return render_template('login.html', success=success)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')


if __name__ == '__main__':
    app.secret_key = 'bauxit'
    app.run(
        debug=True,
        port=5000
    )
