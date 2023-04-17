import sqlalchemy
from sqlalchemy.orm import relationship

Base = sqlalchemy.ext.declarative.declarative_base()


class Person(Base):
    __tablename__ = "person"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(128), nullable=False)
    last_name = sqlalchemy.Column(sqlalchemy.String(128), nullable=False)
    middle_name = sqlalchemy.Column(sqlalchemy.String(128))
    date_of_birth = sqlalchemy.Column(sqlalchemy.String(50), nullable=False)
    sex = sqlalchemy.Column(sqlalchemy.String(30), nullable=False)

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.name = kwargs.get('last_name')
        self.name = kwargs.get('middle_name')
        self.name = kwargs.get('date_of_birth')
        self.name = kwargs.get('sex')

    # marriage = relationship('Marriage', lazy=True)
    death = relationship('Death', backref='person')
    sex_change = relationship('SexChange', backref='person')
    # birth = relationship('Birth', backref='person')
    # adoption = relationship('Adoption', backref='person')
    history = relationship('History', backref='person')
    # genealogy = relationship('Genealogy', backref='person')


class Marriage(Base):
    __tablename__ = "marriage"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    husband_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('person.id'), nullable=False)
    wife_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('person.id'), nullable=False)
    date_of_marriage = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)

    husband = relationship('Person', foreign_keys="Marriage.husband_id")
    wife = relationship('Person', foreign_keys="Marriage.wife_id")

    divorce = relationship('Divorce', backref='marriage')


class Divorce(Base):
    __tablename__ = "divorce"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    marriage_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('marriage.id'), nullable=False)
    date_of_divorce = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)


class Death(Base):
    __tablename__ = "death"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    person_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('person.id'), nullable=False)
    date_of_death = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)


class SexChange(Base):
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    person_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('person.id'), nullable=False)
    date_of_change = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)
    new_sex = sqlalchemy.Column(sqlalchemy.VARCHAR(30), nullable=False)


class Birth(Base):
    __tablename__ = "birth"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    father_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('person.id'), nullable=False)
    mother_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('person.id'), nullable=False)
    child_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('person.id'), nullable=False)
    date_of_birth = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)

    father = relationship('Person', foreign_keys="Birth.father_id")
    mother = relationship('Person', foreign_keys="Birth.mother_id")
    child = relationship('Person', foreign_keys="Birth.child_id")


class Adoption(Base):
    __tablename__ = "adoption"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    adoptive_father_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('person.id'))
    adoptive_mother_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('person.id'))
    adopted_child_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('person.id'), nullable=False)
    date_of_adopt = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)

    adoptive_father = relationship('Person', foreign_keys="Adoption.adoptive_father_id")
    adoptive_mother = relationship('Person', foreign_keys="Adoption.adoptive_mother_id")
    adopted_child = relationship('Person', foreign_keys="Adoption.adopted_child_id")


class History(Base):
    __tablename__ = "history"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    person_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('person.id'), nullable=False)
    date_of_change = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)
    changed_parameter = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)
    changed_value = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)


class Genealogy(Base):
    __tablename__ = "genealogy"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    person_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('person.id'), nullable=False)
    parent_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('person.id'), nullable=False)
    generation = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)

    person = relationship('Person', foreign_keys="Genealogy.person_id")
    parent = relationship('Person', foreign_keys="Genealogy.parent_id")
