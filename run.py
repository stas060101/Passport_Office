import subprocess
from passport_office.config import DB_SCRIPT, DB_NAME, PORT, PASSWORD, USER, HOST

db_name = DB_NAME
db_user = USER
port = PORT
host = HOST
password = PASSWORD


def run():
    cmd = [DB_SCRIPT, db_name, db_user, password, host, port]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output, errors = p.communicate()
    if output == f'Database {db_name} created with user {db_user} and password {password}':
        print('Database created successfully')
    else:
        print('Error creating database')


if __name__ == "__main__":
    run()