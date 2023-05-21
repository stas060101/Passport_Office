import typer

from sqlalchemy.exc import DatabaseError

from datetime import datetime

from bulder.builder import Director, FamilyTreeBuilder
from passport_db.db import PassportDB
from passport_office.chain import DataCheck, SexCheck, PersonCheck, MarriageCheck
from passport_office.models import Person, Marriage, Divorce, Death, SexChange, Birth, Adoption, History, Genealogy

db = PassportDB()
app = typer.Typer()


def person_from_db(pers_id) -> int:
    with db.session_scope() as session:
        return session.query(Person).filter_by(id=pers_id).first()


@app.command()
def person_registration(name: str, last_name: str, middle_name: str, date_of_birth: str, sex: str):
    data_check = DataCheck()
    sex_check = SexCheck()
    data_check.set_next(sex_check)
    data_check.check(data=date_of_birth, sex=sex)
    date_of_birth = datetime.strptime(date_of_birth, "%Y-%m-%d")
    person_id = None
    try:
        person = Person(name, last_name, middle_name, date_of_birth, sex)

        with db.session_scope() as session:
            session.add(person)
            session.flush()
            person_id = person.id
            session.commit()

    except DatabaseError:
        db.session_scope.rollback()

    return person_id


# @app.command()
# def get_persons(names: list = None, last_names: list = None, middle_names: list = None):
#     with db.session_scope() as session:
#         query = session.query(Person)
#         if names:
#             query = query.filter(Person.name.in_(names))
#         elif last_names:
#             query = query.filter(Person.last_name.in_(last_names))
#         elif middle_names:
#             query = query.filter(Person.middle_name.in_(middle_names))
#
#         return query.all()


@app.command()
def marriage_registration(husband_id: int, wife_id: int, date_of_marriage: str):
    try:
        data_check = DataCheck()
        person_check = PersonCheck()
        data_check.set_next(person_check)
        data_check.check(db=db, data=date_of_marriage, person_ids=[husband_id, wife_id])
        date_of_marriage = datetime.strptime(date_of_marriage, "%Y-%m-%d")

        marriage = Marriage(husband_id, wife_id, date_of_marriage)

        with db.session_scope() as session:
            session.add(marriage)
            session.commit()

    except DatabaseError:
        db.session.rollback()


def change_marriage_status(marriage_id):
    with db.session_scope() as session:
        marriage = session.query(Marriage).filter_by(id=marriage_id).one()
        marriage.status = "annulled"
        session.flush()
        session.commit()


@app.command()
def divorce_registration(marriage_id: int, date_of_divorce: str):
    try:
        data_check = DataCheck()
        marriage_check = MarriageCheck()
        data_check.set_next(marriage_check)
        data_check.check(db=db, data=date_of_divorce, marriage_id=marriage_id)
        date_of_divorce = datetime.strptime(date_of_divorce, "%Y-%m-%d")
        with db.session_scope() as session:
            marriage = session.query(Marriage).filter_by(id=marriage_id).first()
            additional_data = {
                "date_of_marriage": f"{marriage.date_of_marriage}",
                "duration": f"{date_of_divorce-marriage.date_of_marriage}"
            }

            divorce = Divorce(marriage_id, date_of_divorce, additional_data)

            session.add(divorce)
            change_marriage_status(marriage_id=marriage_id)  # marriage status on db
            session.commit()

    except DatabaseError:
        db.session.rollback()


@app.command()
def death_registration(person_id: int, date_of_death: str):
    data_check = DataCheck()
    person_check = PersonCheck()
    data_check.set_next(person_check)
    data_check.check(db=db, data=date_of_death, person_ids=[person_id])
    date_of_death = datetime.strptime(date_of_death, "%Y-%m-%d")
    try:

        death = Death(person_id, date_of_death)

        with db.session_scope() as session:
            session.add(death)
            session.commit()

    except DatabaseError:
        db.session.rollback()


@app.command()
def sex_change_registration(person_id: int, date_of_change: str, new_sex: str):
    data_check = DataCheck()
    person_check = PersonCheck()
    gender_check = SexCheck()
    data_check.set_next(gender_check).set_next(person_check)
    data_check.check(db=db, data=date_of_change, sex=new_sex, person_ids=[person_id])
    date_of_change = datetime.strptime(date_of_change, "%Y-%m-%d")
    try:

        sex_change = SexChange(person_id, date_of_change, new_sex)

        with db.session_scope() as session:
            session.add(sex_change)
            session.commit()

    except DatabaseError:
        db.session.rollback()


@app.command()
def birth_registration(father_id: int, mother_id: int, date_of_birth: str, child_data: dict):
    # child_registration_id = person_registration(**child_data)
    #
    # data_check = DataCheck()
    # person_check = PersonCheck()
    # data_check.set_next(person_check)
    # data_check.check(db=db, data=date_of_birth, person_ids=[father_id, mother_id, child_registration_id])
    # date_of_birth = datetime.strptime(date_of_birth, "%Y-%m-%d")

    try:

        # birth = Birth(father_id, mother_id, child_registration_id, date_of_birth)

        with db.session_scope() as session:
            # session.add(birth)
            # session.commit()

            child = session.query(Person).filter_by(id=3).one()
            # grand_father = child.birth.father.birth.father.name
            # grand_mother = child.birth.mother.birth.mother.name
            children = child.children
            # grand_father = father.birth.father.name
            # grand_mother = mother.birth.father.name
            print([child.person.name for child in children])

    except DatabaseError:
        db.session.rollback()


@app.command()
def adoption_registration(father_id: int, mother_id: int, child_id: int, date_of_adopt: str):
    data_check = DataCheck()
    person_check = PersonCheck()
    data_check.set_next(person_check)
    data_check.check(db=db, data=date_of_adopt, person_ids=[father_id, mother_id, child_id])
    date_of_adopt = datetime.strptime(date_of_adopt, "%Y-%m-%d")

    try:

        adoption = Adoption(father_id, mother_id, child_id, date_of_adopt)

        with db.session_scope() as session:
            session.add(adoption)
            session.commit()

    except DatabaseError:
        db.session.rollback()


@app.command()
def get_person_history(person_id: int, date_of_change: str, changed_parameter: str, changed_value: str):
    data_check = DataCheck()
    person_check = PersonCheck()
    data_check.set_next(person_check)
    data_check.check(db=db, data=date_of_change, person_ids=[person_id])
    date_of_change = datetime.strptime(date_of_change, "%Y-%m-%d")

    try:
        history = History(person_id, date_of_change, changed_parameter, changed_value)

        with db.session_scope() as session:
            session.add(history)
            session.commit()

    except DatabaseError:
        db.session.rollback()


# TODO: in process
def get_genealogy_tree(person_id: int,  generation: int, format: str):
    try:

        person_check = PersonCheck()
        person_check.check(db=db, person_ids=[person_id])

        director = Director(generation_count=generation)
        builder = FamilyTreeBuilder(person_id=person_id)
        director.builder = builder
        director.build_generation_level()


        #TODO: add strategy export

    except DatabaseError:
        #TODO: db has no attribute like session, need session_scope()
        db.session.rollback()


if __name__ == "__main__":
    app()
