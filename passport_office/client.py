from passport_office.interface import person_registration, adoption_registration, birth_registration, \
    death_registration, marriage_registration, divorce_registration, sex_change_registration, get_person_history, db, \
    get_genealogy_tree
from passport_office.models import Person, SexChange, Adoption

if __name__ == "__main__":
    # person_registration(name='Rozalita',
    #                     last_name='Ivanova',
    #                     middle_name='Abrekovna',
    #                     date_of_birth="1957-07-20",
    #                     sex="woman") #1
    # person_registration(
    #     name='Sasha',
    #     last_name="Shapka",
    #     middle_name="Olegovich",
    #     date_of_birth='1955-07-20',
    #     sex='man'
    # ) #2
    # #
    # marriage_registration(husband_id=2, wife_id=1, date_of_marriage='1980-07-20')
    # birth_registration(father_id=2, mother_id=1, date_of_birth="1980-07-20", child_data={
    #     'name': 'Mariya',
    #     'last_name': 'Shapka',
    #     'middle_name': 'Alexsandrovna',
    #     'date_of_birth': "1980-07-20",
    #     'sex': "woman"
    # }) #3
    #
    # person_registration(name='Ira',
    #                     last_name='Kulesha',
    #                     middle_name='Andriyvna',
    #                     date_of_birth="1957-05-21",
    #                     sex="woman")  # 4
    # person_registration(
    #     name='Mikhaylo',
    #     last_name="Loh",
    #     middle_name="Artemovich",
    #     date_of_birth='1955-05-21',
    #     sex='man'
    # ) #5
    # marriage_registration(husband_id=5, wife_id=4, date_of_marriage='1980-07-20')
    #
    # birth_registration(father_id=5, mother_id=4, date_of_birth="1980-07-20", child_data={
    #     'name': 'Petro',
    #     'last_name': 'Loh',
    #     'middle_name': 'Mikhaylovich',
    #     'date_of_birth': "1980-07-20",
    #     'sex': "man"
    # })  # 6
    #
    # marriage_registration(husband_id=6, wife_id=3, date_of_marriage='2000-07-20')
    # birth_registration(father_id=6, mother_id=3, date_of_birth="2001-07-20", child_data={
    #     'name': 'Sanya',
    #     'last_name': 'Loh',
    #     'middle_name': 'Mikhaylovich',
    #     'date_of_birth': "2001-07-20",
    #     'sex': "man"
    # })#7

    #                     sex="man")#9
    # person_registration(
    #         name='Mikhaylo',
    #         last_name="Loh",
    #         middle_name="Artemovich",
    #         date_of_birth='2020-05-21',
    #         sex='man'
    #     ) #8

    get_genealogy_tree(person_id=7)

    # birth_registration(father_id=2, mother_id=1, date_of_birth="1981-07-20", child_data={
    #     'name': 'Alex',
    #     'last_name': 'Shapka',
    #     'middle_name': 'Alexsandrovich',
    #     'date_of_birth': "1981-07-20",
    #     'sex': "man"
    # })#4
    #
    # person_registration(name='Ira',
    #                     last_name='Kulesha',
    #                     middle_name='Andriyvna',
    #                     date_of_birth="1957-05-21",
    #                     sex="woman")  # 5
    # person_registration(
    #     name='Mikhaylo',
    #     last_name="Loh",
    #     middle_name="Artemovich",
    #     date_of_birth='1955-05-21',
    #     sex='man'
    # ) #6
    #
    # marriage_registration(husband_id=6, wife_id=5, date_of_marriage='2040-07-20')
    # birth_registration(father_id=6, mother_id=5, date_of_birth="1978-09-21", child_data={
    #     'name': 'Lidiya',
    #     'last_name': 'Loh',
    #     'middle_name': 'Mikhailovna',
    #     'date_of_birth': "1978-09-21",
    #     'sex': "woman"
    # })  # 7
    # birth_registration(father_id=6, mother_id=5, date_of_birth="1979-05-21", child_data={
    #     'name': 'Denis',
    #     'last_name': 'Loh',
    #     'middle_name': 'Mikhailovna',
    #     'date_of_birth': "1979-05-21",
    #     'sex': "man"
    # })  # 8
    #
    # person_registration(name='Petro',
    #                     last_name='Amkar',
    #                     middle_name='Serchiyovich',
    #                     date_of_birth="1978-09-21",
    #                     sex="man")#9
    #
    #
    # birth_registration(father_id=9, mother_id=7, date_of_birth="2001-07-20", child_data={
    #     'name': 'Nikita',
    #     'last_name': 'Amkar',
    #     'middle_name': 'Serchiyovich',
    #     'date_of_birth': "2001-07-20",
    #     'sex': "man"
    # })#10
    # person_registration(name='Stanislav',
    #                     last_name='Solovyiv',
    #                     middle_name='Serchiyovich',
    #                     date_of_birth="2001-09-21",



    # divorce_registration(marriage_id=1, date_of_divorce='2045-07-20')


    # adoption_registration(father_id=1, mother_id=2, child_id=3, date_of_adopt="12.03.4.")
    # birth_registration(father_id=1, mother_id=2, child_id=3, date_of_birth="12.03.4.")
    # death_registration(person_id=2, date_of_death='22.02.1970')
    # marriage_registration(6, 2, '25.01.2020')
    # divorce_registration(5, '26.01.2020')
    # sex_change_registration(1, '2021-07-21', 'women')
    # history_add(1, "22.02.2000", 'sex', 'changed to man')
