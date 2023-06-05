""" Conftest module for known vulnerabilities database """

import pytest
from unit_tests.common import Session
from unit_tests.factories import PersonFactory, MarriageFactory
from unit_tests.plugin import db_engine, tables, import_db_models as import_models


@pytest.fixture()
def marriage_registration(db, husband_wife_create):
    couple = {'date_of_marriage': "2015-10-23"}
    for person in husband_wife_create:
        if person.sex == "man":
            couple.update({'husband_id': person.id})
        else:
            couple.update({'wife_id': person.id})

    marriage = MarriageFactory.create(**couple)
    db.add(marriage)
    db.commit()
    return {"id": marriage.id, "husband_id": marriage.husband_id, "wife_id": marriage.wife_id,
            "date_of_marriage": marriage.date_of_marriage}


@pytest.fixture()
def create_person(db):
   db_data = {'name': 'Vova',
              'last_name': 'Pupkin',
              'middle_name': 'Fedorovich',
              'date_of_birth': '1991-12-13',
              'sex': 'man'}

   person = PersonFactory.create(**db_data)
   db.add(person)
   db.commit()

   return {"id": person.id, "name": person.name,
           "last_name": person.last_name, "middle_name": person.middle_name,
           "date_of_birth": person.date_of_birth}


@pytest.fixture()
def husband_wife_create(db):
    set_data = [{'name': 'Vova',
                 'last_name': 'Pupkin',
                 'middle_name': 'Fedorovich',
                 'date_of_birth': '1991-12-13',
                 'sex': 'man'},
                {
                    'name': 'Mariya',
                    'last_name': 'Pupkin',
                    'middle_name': 'Fedorovna',
                    'date_of_birth': '1991-12-13',
                    'sex': 'woman'
                }]
    cople = []
    for set in set_data:
        person = PersonFactory.create(**set)
        db.add(person)
        db.commit()
        cople.append(person)
    return cople


@pytest.fixture
def mock_session(db):
    session = db
    return session


@pytest.fixture()
def db_data():
    return {
        'name': 'Vova',
        'last_name': 'Pupkin',
        'middle_name': 'Fedorovich',
        'date_of_birth': '1991-12-13',
        'sex': 'man'
        }


@pytest.fixture(scope="session")
def import_db_models(import_models):
    models = import_models

    from passport_office.models import Person, Marriage, Adoption, Birth, Death, Divorce, Child, SexChange, History
    extending_models = [Person, Marriage, Adoption, Birth, Death, Divorce, Child, SexChange, History]

    models.extend(extending_models)

    return models


@pytest.fixture
def db(db_engine, tables):
    """Fixture for initializing the DB."""

    connection = db_engine.connect()
    db_engine.begin()
    Session.configure(bind=connection)

    session = Session()
    yield session

    Session.remove()