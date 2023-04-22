# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy

# from passport_office.config import SQLALCHEMY_DATABASE_URI


# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
#
# db = SQLAlchemy(app)

from passport_office import models, connection_db
