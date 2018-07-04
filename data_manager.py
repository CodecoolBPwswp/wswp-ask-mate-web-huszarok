'''Connection layer between the server and the data.
Functions here should be called from the server.py and these should use generic functions from the connection.py'''

import connection
import datetime
from operator import itemgetter
import util


def get_questions_from_file():
    list_of_questions = connection.get_data_from_file('sample_data/question.csv')
    return list_of_questions


def append_question_from_server():
    pass
    id = util.generate_id('question')   #megnézi, hogy questionhöz vagy answershez kell új id-t generálni
    #date = generate_timestamp()   aktuális dátum adatait lekéri majd UNIX formátumba konvertálja
    #0: egyelőre default érték a Vote-hoz és a View-hoz
    # title, message: a servertől érkező adatok
    #vmi ilyesmi lesz: [id,date,0,0,title, message]
    #ezt a listát kell továbbadni a connection.py-nak és dictwriterrel hozzáírni a csv fájlhoz


def generate_timestamp():
    pass


def get_answers_from_file():
    list_of_answers = connection.get_data_from_file('sample_data/answer.csv')
    return list_of_answers


def convert_timestamp_to_date(timestamp):
    time = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
    return time


def sort_questions_by_date(title, reverse):
    title_to_convert_to_number = ['id','submission_time','view_number','vote_number']
    list_of_questions = get_questions_from_file()

    for question in list_of_questions:
        for key in question:
            if key in title_to_convert_to_number:
                question[key] = int(question[key])

    list_of_questions = sorted(list_of_questions, key=itemgetter(title), reverse=reverse)
    for question in list_of_questions:
        question['submission_time'] = convert_timestamp_to_date(question['submission_time'])
    return list_of_questions

