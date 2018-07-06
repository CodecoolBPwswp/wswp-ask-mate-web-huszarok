'''Connection layer between the server and the data.
Functions here should be called from the server.py and these should use generic functions from the connection.py'''

import connection
import datetime
from operator import itemgetter
import util
import time


def get_questions_from_file():
    list_of_questions = connection.get_data_from_file('sample_data/question.csv')
    return list_of_questions


def get_answer_from_file():
    list_of_answers = connection.get_data_from_file('sample_data/answer.csv')
    return list_of_answers


def append_question_from_server(title, message):
    question_data = [util.generate_id('question'),
                     generate_timestamp(),
                     0,
                     0,
                     title,
                     message]
    connection.append_data_to_file('sample_data/question.csv', question_data)
    return question_data[0]


def update_question_from_server(title, message, question_data):
    updated_question_data = question_data
    updated_question_data['title'] = title
    updated_question_data['message'] = message
    connection.update_data_in_file('sample_data/question.csv', updated_question_data)


def update_answer_from_server(message, answer_data):
    updated_answer_data = answer_data
    updated_answer_data['message'] = message
    connection.update_data_in_file('sample_data/answer.csv', updated_answer_data)


def append_answer_from_server(question_id, message):
    answer_data = [util.generate_id('answer'),  # question id
                   generate_timestamp(),        # submission time
                   0,                           # vote number
                   question_id,                 # question id
                   message]                     # message
    connection.append_data_to_file('sample_data/answer.csv', answer_data)
    return answer_data[0]


def generate_timestamp():
    return int(time.time())


def get_answers_from_file():
    list_of_answers = connection.get_data_from_file('sample_data/answer.csv')
    return list_of_answers


def convert_timestamp_to_date(timestamp):
    time = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
    return time


def sort_questions_by_date(title, reverse):
    title_to_convert_to_number = ['id', 'view_number', 'vote_number']
    list_of_questions = get_questions_from_file()

    for question in list_of_questions:
        for key in question:
            if key in title_to_convert_to_number:
                question[key] = int(question[key])
            if key == 'submission_time':
                try:
                    question[key] = int(question[key])
                except ValueError:
                    date_time = question[key]
                    pattern = '%Y-%m-%d %H:%M:%S'
                    question[key] = int(time.mktime(time.strptime(date_time, pattern)))

        question['submission_time'] = convert_timestamp_to_date(question['submission_time'])

    list_of_questions = sorted(list_of_questions, key=itemgetter(title), reverse=reverse)


    return list_of_questions


def sort_answer_by_date(title, reverse):
    title_to_convert_to_number = ['id','submission_time','view_number','vote_number', 'question_id']
    list_of_answers = get_answer_from_file()

    for answer in list_of_answers:
        for key in answer:
            if key in title_to_convert_to_number:
                answer[key] = int(answer[key])

    list_of_answers = sorted(list_of_answers, key=itemgetter(title), reverse=reverse)
    for answer in list_of_answers:
        answer['submission_time'] = convert_timestamp_to_date(answer['submission_time'])
    return list_of_answers


def from_dict_to_variable(dict, dict_id, question_id):
    for dict_items in dict:
        for key, value in dict_items.items():
            if dict_items[dict_id] == question_id:
                question = dict_items
                return question


def vote(question_data):
    for key in question_data:
        if key == 'id':
            question_data[key] = str(question_data[key])

    connection.update_data_in_file('sample_data/question.csv', question_data)