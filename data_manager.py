'''Connection layer between the server and the data.
Functions here should be called from the server.py and these should use generic functions from the connection.py'''

import connection

def get_questions_from_file():
    list_of_questions = connection.get_data_from_file('sample_data/question.csv')
    return list_of_questions


def get_answers_from_file():
    list_of_answers = connection.get_data_from_file('answer.csv')
    return list_of_answers

