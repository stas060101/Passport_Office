from passport_office.interface import person_registration, adoption_registration, birth_registration, \
    death_registration, marriage_registration, divorce_registration, sex_change_registration, get_person_history, db
from passport_office.models import Person, SexChange, Adoption

if __name__ == "__main__":
    person_registration(name='Rozalitaaaaaa',
                        last_name='Shapka',
                        middle_name='Abrekovna',
                        date_of_birth="2021-07-20",
                        sex="woman")
    person_registration(
        name='Sasha',
        last_name="Shapka",
        middle_name="Olegovich",
        date_of_birth='2021-07-20',
        sex='man'
    )

    marriage_registration(husband_id=1, wife_id=2, date_of_marriage='2040-07-20')

    # adoption_registration(father_id=1, mother_id=2, child_id=3, date_of_adopt="12.03.4.")
    # birth_registration(father_id=1, mother_id=2, child_id=3, date_of_birth="12.03.4.")
    # death_registration(person_id=2, date_of_death='22.02.1970')
    # marriage_registration(6, 2, '25.01.2020')
    # divorce_registration(5, '26.01.2020')
    # sex_change_registration(1, '2021-07-21', 'women')
    # history_add(1, "22.02.2000", 'sex', 'changed to man')
