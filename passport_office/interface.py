from datetime import datetime

from sqlalchemy.exc import DatabaseError, NoResultFound

from passport_office import db
from passport_office.models import Person, Marriage, Divorce, Death, SexChange, Birth, Adoption, History, Genealogy


def db_add(instance):
    db.session.add(instance)
    db.session.commit()


def db_remove(instance):
    db.session.delete(instance)
    db.session.commit()


def person_from_db_id(pers_id) -> int:
    return (Person.query.filter_by(id=pers_id).first()).id


def person_registration(name: str, last_name: str, middle_name: str, date_of_birth: datetime, sex: str):
    try:
        person = Person(name, last_name, middle_name, date_of_birth, sex)
        db_add(person)

    except DatabaseError:
        db.session.rollback()


def marriage_registration(husband_id: int, wife_id: int, date_of_marriage: datetime):
    try:
        husband_db_id = person_from_db_id(husband_id)
        wife_db_id = person_from_db_id(wife_id)

        if not husband_db_id:
            raise Exception('No husband_db_id were found for "marriage_registration" func')
        if not wife_db_id:
            raise Exception('No wife_db_id were found for "marriage_registration" func')

        marriage = Marriage(husband_db_id, wife_db_id, date_of_marriage)
        db_add(marriage)

    except DatabaseError:
        db.session.rollback()


def divorce_registration(marriage_id: int, date_of_divorce: datetime):
    try:
        marriage_db_id = (Marriage.query.filter_by(id=marriage_id).first()).id

        if not marriage_db_id:
            raise Exception('No marriage_id was found for "divorce_registration" func')

        divorce = Divorce(marriage_db_id, date_of_divorce)
        db_add(divorce)

    except DatabaseError:
        db.session.rollback()


def annulment_marriage(marriage_id: str):
    try:
        try:
            marriage_obj = Marriage.query.filter_by(id=marriage_id).first()
            db_remove(marriage_obj)

        except NoResultFound:
            raise Exception('No marriage instance was found in database for "annulment_marriage" func')

    except DatabaseError:
        db.session.rollback()


def death_registration(person_id: str, date_of_death: datetime):
    try:
        person_death_id = person_from_db_id(person_id)
        if not person_death_id:
            raise Exception('No person was found for "death_registration" func')

        death = Death(person_death_id, date_of_death)
        db_add(death)

    except DatabaseError:
        db.session.rollback()


def sex_change_registration(person_id: str, date_of_change: datetime, new_sex: str):
    try:
        person_sex_changing_id = person_from_db_id(person_id)
        if not person_sex_changing_id:
            raise Exception('No person was found for "sex_change_registration" func')

        sex_change = SexChange(person_sex_changing_id, date_of_change, new_sex)
        db_add(sex_change)

    except DatabaseError:
        db.session.rollback()


def birth_registration(father_id: int, mother_id: int, child_id: int, date_of_birth: datetime):
    try:
        father_db_id = person_from_db_id(father_id)
        mother_db_id = person_from_db_id(mother_id)
        child_db_id = person_from_db_id(child_id)

        if not father_db_id:
            raise Exception('No father_db_id was found for "birth_registration" func')
        if not mother_db_id:
            raise Exception('No mother_db_id was found for "birth_registration" func')
        if not child_db_id:
            raise Exception('No child_db_id was found for "birth_registration" func')

        birth = Birth(father_db_id, mother_db_id, child_db_id, date_of_birth)
        db_add(birth)

    except DatabaseError:
        db.session.rollback()


def adoption_registration(father_id: int, mother_id: int, child_id: int, date_of_adopt: datetime):
    try:
        father_db_id = person_from_db_id(father_id)
        mother_db_id = person_from_db_id(mother_id)
        child_db_id = person_from_db_id(child_id)

        if not father_db_id:
            raise Exception('No father_db_id was found for adoption_registration')
        if not mother_db_id:
            raise Exception('No mother_db_id was found for adoption_registration')
        if not child_db_id:
            raise Exception('No child_db_id was found for adoption_registration')

        adoption = Adoption(father_db_id, mother_db_id, child_db_id, date_of_adopt)
        db_add(adoption)

    except DatabaseError:
        db.session.rollback()


def history_add(person_id: int, date_of_change: datetime, changed_parameter: str, changed_value: str):
    try:
        person_db_id = person_from_db_id(person_id)

        if not person_db_id:
            raise Exception('No person was found for "history_add" func')

        history = History(person_db_id, date_of_change, changed_parameter, changed_value)
        db_add(history)

    except DatabaseError:
        db.session.rollback()


def genealogy_add(person_id: int, parent_id: int, generation: int):
    try:
        person_db_id = person_from_db_id(person_id)
        parent_db_id = person_from_db_id(parent_id)

        if not person_db_id:
            raise Exception('No person_db_id was found for "genealogy_add" func')
        if not parent_db_id:
            raise Exception('No parent_db_id was found for "genealogy_add" func')

        genealogy = Genealogy(person_db_id, parent_db_id, generation)
        db_add(genealogy)

    except DatabaseError:
        db.session.rollback()
