import os

DB_NAME = "passport_office"
USER = "sysadmin"
PASSWORD = "passport"
HOST = "127.0.0.1"
PORT = "5432"

DB_SCRIPT = f'/home/{os.getenv("USER")}/passport_office/Passport_Office/passport_db/create_db.sh'
DROP_DB_SCRIPT = f'/home/{os.getenv("USER")}/passport_office/Passport_Office/passport_db/drop_db.sh'
