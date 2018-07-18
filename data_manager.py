'''Connection layer between the server and the data.
Functions here should be called from the server.py and these should use generic functions from the connection.py'''

import connection
import datetime
from operator import itemgetter
import util
import time
from psycopg2 import sql



@connection.connection_handler
def get_all_data_from_file(cursor, columns, table, order_column, order, limit):
    '''Use this function to access any columns of any table, ordered by any column in any order :)
    give the parameters to this function in server.py
    columns: list of strings, strings are the chosen columns example: ['vote_number', 'title', 'message']
    table: table name as string  example: 'question'
    order_by: column name as string  example: 'submission_time'
    order: 'ASC' or 'DESC'
    limit: integer or None (None means ALL)
    '''
    used_columns = sql.SQL(', ').join(sql.Identifier(n) for n in columns)
    if order == 'DESC':
        cursor.execute(
            sql.SQL("""SELECT {col} FROM {table} 
                    ORDER BY {order_column} DESC
                    LIMIT {limit_value} """)
                .format(col= used_columns,
                        table=sql.Identifier(table),
                        order_column=sql.Identifier(order_column),
                        limit_value=sql.Literal(limit))
        )
    elif order == 'ASC':
        cursor.execute(
            sql.SQL("""SELECT {col} FROM {table} 
                    ORDER BY {order_column} ASC
                    LIMIT {limit_value} """)
                .format(col=used_columns,
                        table=sql.Identifier(table),
                        order_column=sql.Identifier(order_column),
                        limit_value=sql.Literal(limit))
        )
    list_of_data = cursor.fetchall()
    return list_of_data


@connection.connection_handler
def get_data_by_id(cursor, columns, table, data_id):
    used_columns = sql.SQL(', ').join(sql.Identifier(n) for n in columns)
    sql_query = sql.SQL("""SELECT {col}
                           FROM {table} 
                           WHERE id = {data_id} """)\
        .format(col=used_columns, table=sql.Identifier(table), data_id=sql.Literal(data_id))
    cursor.execute(sql_query)

    data = cursor.fetchone()

    return data


@connection.connection_handler
def get_comments_by_id(cursor, columns, table, data_id):
    used_columns = sql.SQL(', ').join(sql.Identifier(n) for n in columns)
    sql_query = sql.SQL("""SELECT {col}
                           FROM {table} 
                           WHERE question_id = {data_id} """)\
        .format(col=used_columns, table=sql.Identifier(table), data_id=sql.Literal(data_id))
    cursor.execute(sql_query)

    data = cursor.fetchall()

    return data


@connection.connection_handler
def update_data(cursor, column, table, value, data_id):
    cursor.execute(
        sql.SQL("""UPDATE {table} 
                SET {col} = {value}
                WHERE id = {data_id}""").format(col=sql.Identifier(column),
                                                table=sql.Identifier(table),
                                                value=value),
                                                data_id=sql.Literal(data_id)
    )


@connection.connection_handler
def delete_comments(cursor, table, data_id):
    cursor.execute(
        sql.SQL("""DELETE FROM {table}
                    WHERE id={data_id}""")
                .format(table=sql.Identifier(table),
                        data_id=sql.Literal(data_id)))


@connection.connection_handler
def comment_update(cursor, messages, question_id, table):
    cursor.execute(
            sql.SQL("""
                    INSERT INTO {table}
                    VALUES (DEFAULT, %s, NULL, %s, now(), %s)
                    """)
                .format(
                        table=sql.Identifier(table),
                        question_id=question_id,
                        messages=messages),
                        [question_id, messages, 0]
)


@connection.connection_handler
def answer_question(cursor, message, question_id, table):
    query = """INSERT INTO {table} (id, submission_time, vote_number,
                                                 question_id, message, image)
                            VALUES (DEFAULT, now(), 0, {question_id}, %(text)s, NULL)
                            """
    composed_query = sql.SQL(query).format(
                                         table=sql.Identifier(table),
                                         question_id=sql.Literal(question_id))
    cursor.execute(composed_query, {"text": message})


@connection.connection_handler
def add_tag(cursor, question_id, table, tag):
    cursor.execute(
        sql.SQL("""
                        INSERT INTO {table} (id, name)
                        VALUES (DEFAULT, %s)
                        """)
            .format(
            table=sql.Identifier(table),
            question_id=question_id,
            tag=tag),
                [tag])


@connection.connection_handler
def get_tags_name(cursor):
    cursor.execute(
        sql.SQL("""
                SELECT name FROM tag""")
    )
    tags = cursor.fetchall()
    return tags


def append_question_from_server(title, message):
    question_data = [util.generate_id('question'),
                     generate_timestamp(),
                     0,
                     0,
                     title,
                     message]
    connection.append_data_to_file('sample_data/question.csv', question_data)
    return question_data[0]


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