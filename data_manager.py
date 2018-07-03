'''Connection layer between the server and the data.
Functions here should be called from the server.py and these should use generic functions from the connection.py'''

import connection
import datetime
from operator import itemgetter

def get_questions_from_file():
    list_of_questions = connection.get_data_from_file('sample_data/question.csv')
    return list_of_questions


def get_answers_from_file():
    list_of_answers = connection.get_data_from_file('answer.csv')
    return list_of_answers


def convert_submission_time_to_date(timestamp):
    time = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
    return time


def sort_questions_by_date():
    list_of_questions = get_questions_from_file()
    list_of_questions = sorted(list_of_questions, key=itemgetter('submission_time'), reverse=True)
    for question in list_of_questions:
        question['submission_time'] = convert_submission_time_to_date(question['submission_time'])
    return list_of_questions

