""" Common module for handling SQLAlchemy DB sessions """


from sqlalchemy import orm

Session = orm.scoped_session(orm.sessionmaker())