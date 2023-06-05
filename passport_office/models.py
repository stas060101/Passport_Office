from typing import List

import sqlalchemy
from sqlalchemy.event import listens_for
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Person(Base):
    __tablename__ = "person"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(128), nullable=False)
    last_name = sqlalchemy.Column(sqlalchemy.String(128), nullable=False)
    middle_name = sqlalchemy.Column(sqlalchemy.String(128))
    date_of_birth = sqlalchemy.Column(sqlalchemy.DateTime(), nullable=False)
    sex = sqlalchemy.Column(sqlalchemy.String(30), nullable=False)

    children: Mapped[List["Child"]] = relationship(back_populates='parent', primaryjoin="or_(Person.id==Child.father_id,\
     Person.id==Child.mother_id)")
    changed_sex: Mapped[List["SexChange"]] = relationship(back_populates="person")
    marriage: Mapped["Marriage"] = relationship(back_populates='person', primaryjoin="or_(Person.id==Marriage.husband_id, Person.id==Marriage.wife_id)")
    death: Mapped["Death"] = relationship(back_populates='person')
    birth: Mapped["Birth"] = relationship(back_populates='person', primaryjoin="or_(Person.id==Birth.father_id,\
     Person.id==Birth.mother_id, Person.id==Birth.child_id)")
    history: Mapped["History"] = relationship(back_populates="person")
    adoption: Mapped[List["Adoption"]] = relationship(back_populates='person', primaryjoin="or_(Person.id==Adoption.adoptive_father_id,\
     Person.id==Adoption.adoptive_mother_id, Person.id==Adoption.adopted_child_id)")

    def __init__(self, name, last_name, middle_name, date_of_birth, sex):
        self.name = name.capitalize()
        self.last_name = last_name.capitalize()
        self.middle_name = middle_name.capitalize()
        self.date_of_birth = date_of_birth
        self.sex = sex


@listens_for(Person, 'after_insert')
def add_history(mapper, connection, target):
    connection.execute(
        History.__table__.insert().values(person_id=target.id,
                                          date_of_change=target.date_of_birth,
                                          changed_parameter="person_registration",
                                          changed_value=None)
    )


class Marriage(Base):
    __tablename__ = "marriage"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    husband_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('person.id'), nullable=False)
    wife_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('person.id'), nullable=False)
    date_of_marriage = sqlalchemy.Column(sqlalchemy.DateTime(), nullable=False)
    status = sqlalchemy.Column(sqlalchemy.String(15), nullable=False)

    husband = relationship('Person', foreign_keys=[husband_id], back_populates='marriage')
    wife = relationship('Person', foreign_keys=[wife_id], back_populates='marriage')
    person = relationship('Person', back_populates='marriage', foreign_keys=[husband_id, wife_id],
                          primaryjoin="or_(Person.id==Marriage.husband_id, Person.id==Marriage.wife_id)")

    divorce: Mapped["Divorce"] = relationship(back_populates="marriage")

    def __init__(self, husband_id, wife_id, date_of_marriage):
        self.husband_id = husband_id
        self.wife_id = wife_id
        self.date_of_marriage = date_of_marriage
        self.status = 'active'


@listens_for(Marriage, 'after_insert')
def add_history(mapper, connection, target):
    target_ids = [target.husband_id, target.wife_id]
    for target_id in target_ids:
        connection.execute(
            History.__table__.insert().values(person_id=target_id,
                                              date_of_change=target.date_of_marriage,
                                              changed_parameter="marriage",
                                              changed_value=None)
        )


class Divorce(Base):
    __tablename__ = "divorce"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    marriage_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('marriage.id'), nullable=False)
    date_of_divorce = sqlalchemy.Column(sqlalchemy.DateTime(), nullable=False)
    additional_data = sqlalchemy.Column(sqlalchemy.JSON())

    marriage: Mapped["Marriage"] = relationship(foreign_keys=marriage_id, back_populates="divorce")

    def __init__(self, marriage_id, date_of_divorce, additional_data):
        self.marriage_id = marriage_id
        self.date_of_divorce = date_of_divorce
        self.additional_data = additional_data


@listens_for(Divorce, 'after_insert')
def add_history(mapper, connection, target):
    res = connection.execute(sqlalchemy.text(f"SELECT husband_id, wife_id FROM marriage WHERE marriage.id = {target.marriage_id}")).fetchall()
    target_ids = [res[0][0], res[0][1]]
    for target_id in target_ids:
        connection.execute(
            History.__table__.insert().values(person_id=target_id,
                                              date_of_change=target.date_of_divorce,
                                              changed_parameter="divorce",
                                              changed_value=None)
        )


class Death(Base):
    __tablename__ = "death"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    person_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('person.id'), nullable=True)
    date_of_death = sqlalchemy.Column(sqlalchemy.DateTime(), nullable=False)

    person: Mapped["Person"] = relationship(back_populates="death")

    def __init__(self, person_id, date_of_death):
        self.person_id = person_id
        self.date_of_death = date_of_death


@listens_for(Death, 'after_insert')
def add_history(mapper, connection, target):
    target_id = target.person_id
    connection.execute(
        History.__table__.insert().values(person_id=target_id,
                                          date_of_change=target.date_of_death,
                                          changed_parameter="death",
                                          changed_value=None)
    )


class SexChange(Base):
    __tablename__ = "person_sex_change"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    person_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('person.id'), nullable=False)
    date_of_change = sqlalchemy.Column(sqlalchemy.DateTime(), nullable=False)
    new_sex = sqlalchemy.Column(sqlalchemy.String(30), nullable=False)

    person: Mapped["Person"] = relationship(back_populates='changed_sex')

    def __init__(self, person_id, date_of_change, new_sex):
        self.person_id = person_id
        self.date_of_change = date_of_change
        self.new_sex = new_sex


@listens_for(SexChange, 'after_insert')
def add_history(mapper, connection, target):
    target_id = target.person_id
    connection.execute(
        History.__table__.insert().values(person_id=target_id,
                                          date_of_change=target.date_of_change,
                                          changed_parameter="sex_change",
                                          changed_value=target.new_sex)
    )


class Child(Base):
    __tablename__ = 'child'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    person_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('person.id'), nullable=False)
    mother_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('person.id'), nullable=False)
    father_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('person.id'), nullable=False)
    parent: Mapped["Person"] = relationship(back_populates='children', foreign_keys=[father_id, mother_id],
                                            primaryjoin="or_(Person.id==Child.father_id, Person.id==Child.mother_id)")
    person: Mapped["Person"] = relationship(foreign_keys=person_id)


class Birth(Base):
    __tablename__ = "birth"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    father_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('person.id'), nullable=False)
    mother_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('person.id'), nullable=False)
    child_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('person.id'), nullable=False)
    date_of_birth = sqlalchemy.Column(sqlalchemy.DateTime(), nullable=False)

    father = relationship('Person', foreign_keys=[father_id], back_populates='birth')
    mother = relationship('Person', foreign_keys=[mother_id], back_populates='birth')
    child = relationship('Person', foreign_keys=[child_id], back_populates='birth')

    person = relationship('Person', back_populates='birth', foreign_keys=[father_id, mother_id, child_id],
                          primaryjoin="or_(Person.id==Birth.father_id, Person.id==Birth.mother_id, Person.id==Birth.child_id)")

    def __init__(self, father_id, mother_id, child_id, date_of_birth):
        self.father_id = father_id
        self.mother_id = mother_id
        self.child_id = child_id
        self.date_of_birth = date_of_birth


@listens_for(Birth, 'after_insert')
def add_birth_to_children(mapper, connection, target):
    child_id = target.child_id
    connection.execute(
        Child.__table__.insert().values(father_id=target.father_id,
                                        mother_id=target.mother_id,
                                        person_id=child_id)
    )


@listens_for(Birth, 'after_insert')
def add_history(mapper, connection, target):
    target_ids = [target.father_id, target.mother_id]
    for target_id in target_ids:
        connection.execute(
            History.__table__.insert().values(person_id=target_id,
                                              date_of_change=target.date_of_birth,
                                              changed_parameter="child birth",
                                              changed_value=target.child_id)
        )


class Adoption(Base):
    __tablename__ = "adoption"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    adoptive_father_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('person.id'))
    adoptive_mother_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('person.id'))
    adopted_child_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('person.id'), nullable=False)
    date_of_adopt = sqlalchemy.Column(sqlalchemy.DateTime(), nullable=False)

    adoptive_father = relationship('Person', foreign_keys=[adoptive_father_id], back_populates='adoption')
    adoptive_mother = relationship('Person', foreign_keys=[adoptive_mother_id], back_populates='adoption')
    adoptive_child = relationship('Person', foreign_keys=[adopted_child_id], back_populates='adoption')

    person = relationship('Person', back_populates='adoption', foreign_keys=[adoptive_father_id, adoptive_mother_id, adopted_child_id],
                          primaryjoin="or_(Person.id==Adoption.adoptive_father_id,\
     Person.id==Adoption.adoptive_mother_id, Person.id==Adoption.adopted_child_id)")

    def __init__(self, adoptive_father_id, adoptive_mother_id, adopted_child_id, date_of_adopt):
        self.adoptive_father_id = adoptive_father_id
        self.adoptive_mother_id = adoptive_mother_id
        self.adopted_child_id = adopted_child_id
        self.date_of_adopt = date_of_adopt


@listens_for(Adoption, 'after_insert')
def add_history(mapper, connection, target):
    target_ids = [target.adoptive_father_id, target.adoptive_mother_id]
    for target_id in target_ids:
        connection.execute(
            History.__table__.insert().values(person_id=target_id,
                                              date_of_change=target.date_of_adopt,
                                              changed_parameter="adopted child",
                                              changed_value=target.adopted_child_id)
        )


class History(Base):
    __tablename__ = "history"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    person_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('person.id'), nullable=False)
    date_of_change = sqlalchemy.Column(sqlalchemy.DateTime(), nullable=False)
    changed_parameter = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)
    changed_value = sqlalchemy.Column(sqlalchemy.String(100), nullable=True)

    person: Mapped["Person"] = relationship(back_populates="history")

    def __init__(self, person_id, date_of_change, changed_parameter, changed_value):
        self.person_id = person_id
        self.date_of_change = date_of_change
        self.changed_parameter = changed_parameter
        self.changed_value = changed_value