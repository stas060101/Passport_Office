from passport_office.interface import person_registration, adoption_registration, birth_registration, \
    death_registration, marriage_registration, divorce_registration, sex_change_registration, history_add

if __name__ == "__main__":
    # person_registration(name='Rozalitaaaa',
    #                     last_name='Shapka',
    #                     middle_name='Abrekovna',
    #                     date_of_birth="20.07.2001",
    #                     sex="women")
    # adoption_registration(father_id=1, mother_id=2, child_id=3, date_of_adopt="12.03.4.")
    # birth_registration(father_id=1, mother_id=2, child_id=3, date_of_birth="12.03.4.")
    # death_registration(person_id=2, date_of_death='22.02.1970')
    # marriage_registration(6, 2, '25.01.2020')
    divorce_registration(5, '26.01.2020')
    # sex_change_registration(1, '26.01.2020', 'man')
    # history_add(1, "22.02.2000", 'sex', 'changed to man')
