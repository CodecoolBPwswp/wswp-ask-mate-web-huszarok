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


def generate_timestamp():
    return int(time.time())


def get_answers_from_file():
    list_of_answers = connection.get_data_from_file('sample_data/answer.csv')
    return list_of_answers


def convert_timestamp_to_date(timestamp):
    time = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
    return time


def sort_questions_by_date():
    list_of_questions = get_questions_from_file()
    list_of_questions = sorted(list_of_questions, key=itemgetter('submission_time'), reverse=True)
    for question in list_of_questions:
        question['submission_time'] = convert_timestamp_to_date(question['submission_time'])
    return list_of_questions

