import psycopg2

conn = psycopg2.connect(host="localhost", port = 5432, database="ligataxi", user="dmitriy")
cur = conn.cursor()
print("Database opened successfully")

# class BD1:
#
#     def ss(self):
#         cur.execute("""SELECT * FROM subscr""")
#         query_results = cur.fetchall()
#         text = '\n\n'.join([', '.join(map(str, x)) for x in query_results])
#         return (str(text))


