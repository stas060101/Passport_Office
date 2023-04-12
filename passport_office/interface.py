from passport_office import db
from passport_office.models import Person, Marriage, Divorce


def add_person(name, last_name, middle_name, date_of_birth, sex):

    person = Person(
        name=name,
        last_name=last_name,
        middle_name=middle_name,
        date_of_birth=date_of_birth,
        sex=sex
    )

    db.session.add(person)
    db.session.commit()


def marriage_status(husband_id, wife_id, date_of_marriage):

    marriage = Marriage(
        husband_id=husband_id,
        wife_id=wife_id,
        date_of_marriage=date_of_marriage
    )

    db.session.add(marriage)
    db.session.commit()


# def marriage_add(hus_id, wif_id, date_of_marriage):
#
#     husband_id = (Person.query.filter_by(id=hus_id).first()).id
#     wife_id = (Person.query.filter_by(id=wif_id).first()).id
#
#     marriage = Marriage(
#         husband_id=husband_id,
#         wife_id=wife_id,
#         date_of_marriage=date_of_marriage
#     )
#
#     db.session.add(marriage)
#     db.session.commit()


def divorce_add(marriage_id, date_of_divorce):

    divorce = Divorce(
        marriage_id=marriage_id,
        date_of_divorce=date_of_divorce
    )

    db.session.add(divorce)
    db.session.commit()