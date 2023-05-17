import subprocess
from passport_office.config import DB_SCRIPT, DROP_DB_SCRIPT, DB_NAME, PORT, PASSWORD, USER, HOST

db_name = DB_NAME
db_user = USER
port = PORT
host = HOST
password = PASSWORD


def extend_db_by_models():
    from passport_db.db import PassportDB

    db_instance = PassportDB(create_all=True)


def run(drop=False):
    if drop:
        cmd = [DROP_DB_SCRIPT, db_name, db_user, password, host, port]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output, errors = p.communicate()
        if (output.decode()).split('\n')[0] == "DROP DATABASE" and (output.decode()).split('\n')[1] == "REASSIGN OWNED"\
                and (output.decode()).split('\n')[2] == "DROP OWNED" and (output.decode()).split('\n')[3] == "DROP ROLE":
            print(f'Database {db_name} dropped with user {db_user} and password {password}')
            print("Database successfully dropped")

        elif (output.decode()).split('\n')[0] == 'ERROR:  database "passport_office" is being accessed by other users':
            print("Database is using by another users")

    # create_db
    cmd = [DB_SCRIPT, db_name, db_user, password, host, port]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output, errors = p.communicate()
    if (output.decode()).split('\n')[0] == "CREATE DATABASE" and (output.decode()).split('\n')[1] == "CREATE ROLE" and \
            (output.decode()).split('\n')[2] == "GRANT":
        print(f'Database {db_name} created with user {db_user} and password {password}')
        extend_db_by_models()
        print('Database extend successfully')
    elif (output.decode()).split('\n')[0] == f'ERROR:  database "{db_name}" already exists':
        print(f'Database {db_name} is already exists')


if __name__ == "__main__":
    run(drop=True)
