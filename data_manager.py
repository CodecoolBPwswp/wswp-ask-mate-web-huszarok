import connection
from psycopg2 import sql



@connection.connection_handler
def get_all_data_from_file(cursor, columns, table, order_column, order, limit):
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
def get_data_by_id(cursor, columns, table, question_id, id_type):
    used_columns = sql.SQL(', ').join(sql.Identifier(n) for n in columns)
    sql_query = sql.SQL("""SELECT {col}
                           FROM {table} 
                           WHERE {id_type} = {data_id} """)\
        .format(col=used_columns,
                table=sql.Identifier(table),
                data_id=sql.Literal(question_id),
                id_type=sql.Identifier(id_type))
    cursor.execute(sql_query)

    data = cursor.fetchall()

    return data


@connection.connection_handler
def get_data_by_search(cursor, columns, table, phrase):
    phrase = '%' + phrase + '%'
    comprehension = [sql.SQL('.').join([sql.Identifier(table), sql.Identifier(n)]) for n in columns]
    used_columns = sql.SQL(', ').join(comprehension)
    sql_query = sql.SQL("""SELECT {col}
                           FROM question
                           FULL JOIN answer ON question.id=answer.question_id
                           WHERE (question.title LIKE lower({phrase}) OR 
                           question.message LIKE lower({phrase}) OR
                           answer.message LIKE lower({phrase})); """)\
        .format(col=used_columns,
                table=sql.Identifier(table),
                phrase=sql.Literal(phrase))
    print(sql_query.as_string(cursor))
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
def answer_comment_update(cursor, messages, answer_id, table):
    cursor.execute(
            sql.SQL("""
                    INSERT INTO {table}
                    VALUES (DEFAULT, NULL, %s, %s, now(), %s)
                    """)
                .format(
                        table=sql.Identifier(table),
                        answer_id=answer_id,
                        messages=messages),
                        [answer_id, messages, 0]
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
def get_id_question_or_answer(cursor, q_id):
    cursor.execute("""
                    SELECT id 
                    FROM answer
                    WHERE question_id=%(q_id)s;
                    """,
                    {'q_id': q_id})
    data = cursor.fetchall()

    return data


def append_answer_from_server(question_id, message):
    answer_data = [util.generate_id('answer'),  # question id
                   generate_timestamp(),        # submission time
                   0,                           # vote number
                   question_id,                 # question id
                   message]                     # message
    connection.append_data_to_file('sample_data/answer.csv', answer_data)
    return answer_data[0]
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


@connection.connection_handler
def add_question(cursor, title, message):
    query = sql.SQL("""INSERT INTO question 
            (id, submission_time, view_number, vote_number, title, message, image)
            VALUES (DEFAULT, now(), 0, 0, %(title)s, %(message)s, NULL)""")
    cursor.execute(query, {'title':title, 'message':message})



def vote(question_data):
    for key in question_data:
        if key == 'id':
            question_data[key] = str(question_data[key])

    connection.update_data_in_file('sample_data/question.csv', question_data)