'''Connection layer between the server and the data.
Functions here should be called from the server.py and these should use generic functions from the connection.py'''

import connection
import datetime


def get_questions_from_file():
    list_of_questions = connection.get_data_from_file('sample_data/question.csv')
    for question in list_of_questions:
        question['submission_time'] = convert_submission_time_to_date(question['submission_time'])
    return list_of_questions


def get_answers_from_file():
    list_of_answers = connection.get_data_from_file('answer.csv')
    return list_of_answers


def convert_submission_time_to_date(timestamp):
    time = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
    return time

