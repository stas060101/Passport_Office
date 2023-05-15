from sqlalchemy.exc import DatabaseError

from passport_db.db import PassportDB
from passport_office.models import Person, Marriage, Divorce, Death, SexChange, Birth, Adoption, History, Genealogy

db = PassportDB()


def person_from_db(pers_id) -> int:
    with db.session_scope() as session:
        return session.query(Person).filter_by(id=pers_id).first()


def person_registration(name: str, last_name: str, middle_name: str, date_of_birth: str, sex: str):
    try:
        person = Person(name, last_name, middle_name, date_of_birth, sex)

        with db.session_scope() as session:
            session.add(person)
            session.commit()

    except DatabaseError:
        db.session_scope.rollback()


def marriage_registration(husband_id: int, wife_id: int, date_of_marriage: str):
    try:
        husband_db = person_from_db(husband_id)
        wife_db = person_from_db(wife_id)

        if husband_db is None:
            raise Exception('No husband_db_id were found for "marriage_registration" func')
        if wife_db is None:
            raise Exception('No wife_db_id were found for "marriage_registration" func')

        marriage = Marriage(husband_db.id, wife_db.id, date_of_marriage)

        with db.session_scope() as session:
            session.add(marriage)
            session.commit()

    except DatabaseError:
        db.session.rollback()


def divorce_registration(marriage_id: int, date_of_divorce: str):
    try:
        with db.session_scope() as session:
            marriage_db = session.query(Marriage).filter_by(id=marriage_id).first()

            if marriage_db is None:
                raise Exception('No marriage_id was found for "divorce_registration" func')

            divorce = Divorce(marriage_db.id, date_of_divorce)

            session.add(divorce)
            marriage_db.status = "annulled"  # marriage status on db
            session.commit()

    except DatabaseError:
        db.session.rollback()


def death_registration(person_id: int, date_of_death: str):
    try:
        person_death = person_from_db(person_id)
        if person_death is None:
            raise Exception('No person was found for "death_registration" func')

        death = Death(person_death.id, date_of_death)

        with db.session_scope() as session:
            session.add(death)
            session.commit()

    except DatabaseError:
        db.session.rollback()


def sex_change_registration(person_id: int, date_of_change: str, new_sex: str):
    try:
        person_sex_changing = person_from_db(person_id)
        if person_sex_changing is None:
            raise Exception('No person was found for "sex_change_registration" func')

        sex_change = SexChange(person_sex_changing.id, date_of_change, new_sex)

        with db.session_scope() as session:
            session.add(sex_change)
            session.commit()

    except DatabaseError:
        db.session.rollback()


def birth_registration(father_id: int, mother_id: int, child_id: int, date_of_birth: str):
    try:
        father_db = person_from_db(father_id)
        mother_db = person_from_db(mother_id)
        child_db = person_from_db(child_id)

        if father_db is None:
            raise Exception('No father_db_id was found for "birth_registration" func')
        if mother_db is None:
            raise Exception('No mother_db_id was found for "birth_registration" func')
        if child_db is None:
            raise Exception('No child_db_id was found for "birth_registration" func')

        birth = Birth(father_db.id, mother_db.id, child_db.id, date_of_birth)

        with db.session_scope() as session:
            session.add(birth)
            session.commit()

        # with db.session_scope() as session:
        #     birth = session.query(Birth).all()[0]
        #     name = birth.child.last_name
        #     print(name)

    except DatabaseError:
        db.session.rollback()


def adoption_registration(father_id: int, mother_id: int, child_id: int, date_of_adopt: str):
    try:
        father_db = person_from_db(father_id)
        mother_db = person_from_db(mother_id)
        child_db = person_from_db(child_id)

        if father_db is None:
            raise Exception('No father_db_id was found for adoption_registration')
        if mother_db is None:
            raise Exception('No mother_db_id was found for adoption_registration')
        if child_db is None:
            raise Exception('No child_db_id was found for adoption_registration')

        adoption = Adoption(father_db.id, mother_db.id, child_db.id, date_of_adopt)

        with db.session_scope() as session:
            session.add(adoption)
            session.commit()

        # with db.session_scope() as session:
        #     adoption = session.query(Adoption).all()[0]
        #     name_child = adoption.adoptive_child.name
        #     print(name_child)

    except DatabaseError:
        db.session.rollback()


def history_add(person_id: int, date_of_change: str, changed_parameter: str, changed_value: str):
    try:
        person_db = person_from_db(person_id)

        if person_db is None:
            raise Exception('No person was found for "history_add" func')

        history = History(person_db.id, date_of_change, changed_parameter, changed_value)

        with db.session_scope() as session:
            session.add(history)
            session.commit()

    except DatabaseError:
        db.session.rollback()


def genealogy_add(person_id: int, parent_id: int, generation: int):
    try:
        person_db = person_from_db(person_id)
        parent_db = person_from_db(parent_id)

        if person_db is None:
            raise Exception('No person_db_id was found for "genealogy_add" func')
        if parent_db is None:
            raise Exception('No parent_db_id was found for "genealogy_add" func')

        genealogy = Genealogy(person_db.id, parent_db.id, generation)

        with db.session_scope() as session:
            session.add(genealogy)
            session.commit()

    except DatabaseError:
        db.session.rollback()
