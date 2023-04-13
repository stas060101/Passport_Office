from sqlalchemy.exc import DatabaseError

from passport_office import db
from passport_office.models import Person, Marriage, Divorce


def add_person(name, last_name, middle_name, date_of_birth, sex):
    try:
        # person = Person(name, last_name, middle_name, date_of_birth, sex)
        person = Person(
            name=name,
            last_name=last_name,
            middle_name=middle_name,
            date_of_birth=date_of_birth,
            sex=sex
        )

        if not Person:  # ( if not kwargs in Person) -  перевірка на наявність прийнятих обов'язкових аргументів(доробить)
            raise Exception

        db.session.add(person)
        db.session.commit()

    except DatabaseError:
        db.session.rollback()


def marriage_add(husband_id, wife_id, date_of_marriage):
    try:
        marriage = Marriage(
            husband_id=husband_id,
            wife_id=wife_id,
            date_of_marriage=date_of_marriage
        )

        db.session.add(marriage)
        db.session.commit()

    except DatabaseError:
        db.session.rollback()


# def marriage_add(hus_id, wif_id, date_of_marriage):
#     try:
#         husband_id = (Person.query.filter_by(id=hus_id).first()).id
#         wife_id = (Person.query.filter_by(id=wif_id).first()).id
#
#         marriage = Marriage(
#             husband_id=husband_id,
#             wife_id=wife_id,
#             date_of_marriage=date_of_marriage
#         )
#
#         db.session.add(marriage)
#         db.session.commit()
#
#     except DatabaseError:
#         db.session.rollback()


def divorce_add(marriage_id, date_of_divorce):
    try:
        # add divorce
        divorce = Divorce(
            marriage_id=marriage_id,
            date_of_divorce=date_of_divorce
        )
        db.session.add(divorce)

        # annulment of marriage
        marriage = Marriage.query.filter_by(id=marriage_id).first()
        if not marriage:  # перевірка на наявність marriage в db
            raise Exception

        db.session.delete(marriage)
        db.session.commit()

    except DatabaseError:
        db.session.rollback()


