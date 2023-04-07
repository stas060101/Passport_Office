from psycopg2 import connect, errors

from passport_office import app, db
try:
    conn = connect(
            database="postgres", user='passport_office', password='1234', host='127.0.0.1', port='5432'
        )
    conn.autocommit = True
    cursor = conn.cursor()
    sql = '''CREATE database passport_office'''
    cursor.execute(sql)
    conn.close()

    with app.app_context():
        db.create_all()

except errors.DuplicateDatabase:
    with app.app_context():
        db.create_all()
