from passport_office.interface import person_registration, adoption_registration, birth_registration, \
    death_registration, marriage_registration, divorce_registration, sex_change_registration, get_person_history, db
from passport_office.models import Person, SexChange, Adoption

if __name__ == "__main__":
    person_registration(name='rozalitaaaa',
                        last_name='shapka',
                        middle_name='abrekovna',
                        date_of_birth="2001-07-20",
                        sex="woman")
    # adoption_registration(father_id=1, mother_id=4, child_id=3, date_of_adopt="2002-03-04")
    # birth_registration(father_id=5, mother_id=2, child_id=4, date_of_birth="2001-03-25")
    # death_registration(person_id=2, date_of_death='2002-12-31')
    # marriage_registration(6, 4, '2020-01-01')
    # divorce_registration(6, '2021-03-04')
    # sex_change_registration(1, '2020-01-20', 'man')
    # get_person_history(1, "22.02.2000", 'sex', 'changed to man')
    #
    # with db.session_scope() as session:
    #     sex = session.query(SexChange).filter_by(id=1).first()
    #     a = sex.person_.name
    #     print(a)
    #
