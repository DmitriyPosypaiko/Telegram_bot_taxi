from datetime import date, timedelta
import sqlite3


open("database.db", "w").close()
conn = sqlite3.connect("database.db", check_same_thread=False)

cursor = conn.cursor()

cursor.execute(
    '''
        CREATE TABLE IF NOT EXISTS user (
            id integer PRIMARY KEY,
            first_name text,
            key text
        )
    '''
)


def insert_user_row(row):
    row[1] = str(row[1])
    cursor.execute(
        '''
            INSERT INTO user (first_name, key)
            VALUES(?,?);
        ''',
        row
    )
    conn.commit()


def select_user():
    cursor.execute(
    '''
        SELECT first_name, key FROM user;
    ''',
    )
    results = cursor.fetchall()
    return results

def is_authenticated(row):
    row = str(row[0])
    # print(f'!!!!!!!!!!!!!!!:    {row[0]}')
    cursor.execute(
        f'''
            SELECT key FROM user WHERE key = {row};
        ''',
    )
    results = cursor.fetchall()
    return results

# import psycopg2
#
# conn = psycopg2.connect(host="localhost", port = 5432, database="ligataxi", user="dmitriy")
# cur = conn.cursor()
# print("Database opened successfully")

# class BD1:
#
#     def ss(self):
#         cur.execute("""SELECT * FROM subscr""")
#         query_results = cur.fetchall()
#         text = '\n\n'.join([', '.join(map(str, x)) for x in query_results])
#         return (str(text))


