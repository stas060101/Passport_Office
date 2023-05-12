import sqlalchemy
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
<<<<<<< HEAD
=======

>>>>>>> 2327cbb (add drop_db, fix: config.py, run.py)
Base = declarative_base()


class Person(Base):
    __tablename__ = "person"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(128), nullable=False)
    last_name = sqlalchemy.Column(sqlalchemy.String(128), nullable=False)
    middle_name = sqlalchemy.Column(sqlalchemy.String(128))
    date_of_birth = sqlalchemy.Column(sqlalchemy.String(50), nullable=False)
    sex = sqlalchemy.Column(sqlalchemy.String(30), nullable=False)

    # marriage = relationship('Marriage', lazy=True)
    death = relationship('Death', backref='person')
    sex_change = relationship('SexChange', backref='person')
    # birth = relationship('Birth', backref='person')
    # adoption = relationship('Adoption', backref='person')
    history = relationship('History', backref='person')
    # genealogy = relationship('Genealogy', backref='person')

    def __init__(self, name, last_name, middle_name, date_of_birth, sex):
        self.name = name
        self.last_name = last_name
        self.middle_name = middle_name
        self.date_of_birth = date_of_birth
        self.sex = sex


class Marriage(Base):
    __tablename__ = "marriage"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    husband_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('person.id'), nullable=False)
    wife_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('person.id'), nullable=False)
    date_of_marriage = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)

    husband = relationship('Person', foreign_keys="Marriage.husband_id")
    wife = relationship('Person', foreign_keys="Marriage.wife_id")
    divorce = relationship('Divorce', backref='marriage')

    def __init__(self, husband_id, wife_id, date_of_marriage):
        self.husband_id = husband_id
        self.wife_id = wife_id
        self.date_of_marriage = date_of_marriage


class Divorce(Base):
    __tablename__ = "divorce"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    marriage_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('marriage.id'), nullable=False)
    date_of_divorce = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)

    def __init__(self, marriage_id, date_of_divorce):
        self.marriage_id = marriage_id
        self.date_of_divorce = date_of_divorce


class Death(Base):
    __tablename__ = "death"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    person_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('person.id'), nullable=False)
    date_of_death = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)

    def __init__(self, person_id, date_of_death):
        self.person_id = person_id
        self.date_of_death = date_of_death


class SexChange(Base):
    __tablename__ = "person_sex_change"
<<<<<<< HEAD
=======

>>>>>>> 2327cbb (add drop_db, fix: config.py, run.py)
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    person_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('person.id'), nullable=False)
    date_of_change = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)
    new_sex = sqlalchemy.Column(sqlalchemy.VARCHAR(30), nullable=False)

    def __init__(self, person_id, date_of_change, new_sex):
        self.person_id = person_id
        self.date_of_change = date_of_change
        self.new_sex = new_sex


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

    def __init__(self, father_id, mother_id, child_id, date_of_birth):
        self.father_id = father_id
        self.mother_id = mother_id
        self.child_id = child_id
        self.date_of_birth = date_of_birth


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

    def __init__(self, adoptive_father_id, adoptive_mother_id, adopted_child_id, date_of_adopt):
        self.adoptive_father_id = adoptive_father_id
        self.adoptive_mother_id = adoptive_mother_id
        self.adopted_child_id = adopted_child_id
        self.date_of_adopt = date_of_adopt


class History(Base):
    __tablename__ = "history"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    person_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('person.id'), nullable=False)
    date_of_change = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)
    changed_parameter = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)
    changed_value = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)

    def __init__(self, person_id, date_of_change, changed_parameter, changed_value):
        self.person_id = person_id
        self.date_of_change = date_of_change
        self.changed_parameter = changed_parameter
        self.changed_value = changed_value


class Genealogy(Base):
    __tablename__ = "genealogy"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    person_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('person.id'), nullable=False)
    parent_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('person.id'), nullable=False)
    generation = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)

    person = relationship('Person', foreign_keys="Genealogy.person_id")
    parent = relationship('Person', foreign_keys="Genealogy.parent_id")

    def __init__(self, person_id, parent_id, generation):
        self.person_id = person_id
        self.parent_id = parent_id
        self.generation = generation
