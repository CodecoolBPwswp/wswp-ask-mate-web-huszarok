import connection
from psycopg2 import sql, IntegrityError
import bcrypt



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
def get_data_by_id(cursor, columns, table, data_id, id_type):
    used_columns = sql.SQL(', ').join(sql.Identifier(n) for n in columns)
    sql_query = sql.SQL("""SELECT {col}
                           FROM {table} 
                           WHERE {id_type} = {data_id} """)\
        .format(col=used_columns,
                table=sql.Identifier(table),
                data_id=sql.Literal(data_id),
                id_type=sql.Identifier(id_type))
    cursor.execute(sql_query)

    data = cursor.fetchall()

    return data


@connection.connection_handler
def get_data_by_search(cursor, columns, table, phrase):
    phrase = '%' + phrase + '%'
    comprehension = [sql.SQL('.').join([sql.Identifier(table), sql.Identifier(n)]) for n in columns]
    used_columns = sql.SQL(', ').join(comprehension)
    cursor.execute(sql.SQL("""SELECT {col}
                           FROM question
                           JOIN answer ON question.id=answer.question_id
                           WHERE question.title ILIKE %(phrase)s OR 
                           question.message ILIKE %(phrase)s OR
                           answer.message ILIKE %(phrase)s GROUP BY question.id; """)\
                    .format(col=used_columns,
                            table=sql.Identifier(table)),
                   {'phrase': phrase}
                   )

    data = cursor.fetchall()

    return data


@connection.connection_handler
def update_data(cursor, column, table, value, data_id):
    cursor.execute(
        sql.SQL("""UPDATE {table} 
                SET {col} = %(value)s
                WHERE id = {data_id}""").format(col=sql.Identifier(column),
                                                table=sql.Identifier(table),
                                                data_id=sql.Literal(data_id)),
                                        {'value': value}
    )


@connection.connection_handler
def delete(cursor, table, data_id, id_type):
    cursor.execute(
        sql.SQL("""DELETE FROM {table}
                    WHERE {id_type} = {data_id}""")
                .format(table=sql.Identifier(table),
                        data_id=sql.Literal(data_id),
                        id_type=sql.Identifier(id_type)))


@connection.connection_handler
def add_comment_to_question(cursor, messages, question_id, table):
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
def add_comment_to_answer(cursor, messages, answer_id, table):
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


@connection.connection_handler
def add_tag(cursor, question_id, table, tag):
    cursor.execute(
        sql.SQL("""
                        INSERT INTO {table} (id, name)
                        VALUES (DEFAULT, %s);
                        SELECT id
                        FROM tag
                        ORDER BY id DESC
                        LIMIT 1;
                        """)
            .format(
            table=sql.Identifier(table),
            question_id=sql.Literal(question_id)),
            [tag])
    tag_id = cursor.fetchone()['id']
    cursor.execute(
        sql.SQL("""
                        INSERT INTO question_tag (question_id, tag_id)
                        VALUES ({question_id}, {tag_id})
                        """)
            .format(
            tag_id=sql.Literal(tag_id),
            question_id=sql.Literal(question_id)),
    )


@connection.connection_handler
def get_tags_name(cursor, question_id):
    cursor.execute(
        sql.SQL("""
                SELECT name
                FROM tag
                JOIN question_tag ON tag.id=question_tag.tag_id
                WHERE question_id = {question_id}""")
            .format(
            question_id=sql.Literal(question_id))
    )
    tags = cursor.fetchall()
    return tags


@connection.connection_handler
def add_question(cursor, title, message):
    query = sql.SQL("""INSERT INTO question 
            (id, submission_time, view_number, vote_number, title, message, image)
            VALUES (DEFAULT, now(), 0, 0, %(title)s, %(message)s, NULL)""")
    cursor.execute(query, {'title':title, 'message':message})


@connection.connection_handler
def increment_vote_number(cursor, table, data_id):
    cursor.execute(
        sql.SQL("""UPDATE {table} 
                SET vote_number = vote_number + 1 
                WHERE id = {data_id}""").format(table=sql.Identifier(table),
                                                data_id=sql.Literal(data_id))
    )


@connection.connection_handler
def decrement_vote_number(cursor, table, data_id):
    cursor.execute(
        sql.SQL("""UPDATE {table} 
                SET vote_number = vote_number - 1 
                WHERE id = {data_id}""").format(table=sql.Identifier(table),
                                                data_id=sql.Literal(data_id))
    )



def hash_password(plain_text_password):
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)


@connection.connection_handler
def register(cursor, username, email, password):
    try:
        cursor.execute(
            sql.SQL("""INSERT INTO users
                       VALUES (DEFAULT, %(username)s, %(email)s, %(password)s)
                        """), {'username':username, 'email':email, 'password':password})
        return True
    except IntegrityError:
        return False


@connection.connection_handler
def get_user_data(cursor, username):
    cursor.execute("""SELECT id, username, password
                   FROM users
                   WHERE username=%(username)s 
                    """, {'username': username})

    data = cursor.fetchone()
    return data
