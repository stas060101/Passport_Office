from passport_office.interface import person_registration, marriage_registration, divorce_registration, \
    death_registration, sex_change_registration, birth_registration, adoption_registration, get_person_history
from passport_office.models import Person, Marriage, Divorce, Death, SexChange, Birth, Adoption
from unittest.mock import patch


class TestPersonRegistration:
    def test_person_registration(self, mock_session, db_data):
        with patch("passport_office.interface.db.session_scope", return_value=mock_session):
            person_registration(**db_data)
            person = mock_session.query(Person).filter_by(name=db_data["name"]).one_or_none()
            assert person is not None
            assert person.last_name == db_data["last_name"]
            assert person.middle_name == db_data["middle_name"]
            assert person.sex == db_data["sex"]
            assert person.date_of_birth.strftime("%Y-%m-%d") == db_data["date_of_birth"]


class TestMarriageRegistration:
    def test_marriage_registration(self, husband_wife_create, mock_session):
        with patch("passport_office.interface.db.session_scope", return_value=mock_session):
            for person in husband_wife_create:
                if person.sex == "man":
                    husband_id = person.id
                else:
                    wife_id = person.id

            marriage_registration(husband_id=husband_id, wife_id=wife_id, date_of_marriage='2015-10-23')
            marriage = mock_session.query(Marriage).filter_by(husband_id=husband_id,wife_id=wife_id).one_or_none()
            assert person is not None
            assert marriage.husband_id == husband_id
            assert marriage.wife_id == wife_id
            assert marriage.date_of_marriage.strftime("%Y-%m-%d") == '2015-10-23'


class TestDivorceRegistration:
    def test_divorce_registration(self, mock_session, marriage_registration):
        with patch("passport_office.interface.db.session_scope", return_value=mock_session):
            marriage = marriage_registration
            divorce_registration(marriage_id=marriage["id"], date_of_divorce='2016-10-23')
            divorce = mock_session.query(Divorce).filter_by(marriage_id=marriage["id"]).one_or_none()
            assert divorce is not None
            assert divorce.marriage_id == marriage["id"]
            assert divorce.date_of_divorce.strftime("%Y-%m-%d") == '2016-10-23'


class TestDeathRegistration:

    def test_death_registration(self, mock_session, create_person):
        with patch("passport_office.interface.db.session_scope", return_value=mock_session):
            person_id = create_person["id"]
            death_registration(person_id=person_id, date_of_death='2045-10-23')
            death_record = mock_session.query(Death).filter_by(person_id=person_id).one_or_none()
            assert death_record is not None
            assert death_record.person_id == person_id
            assert death_record.date_of_death.strftime("%Y-%m-%d") == '2045-10-23'


class TestSexChangeRegistration:
     def test_sex_change_registration(self,mock_session, create_person):
        with patch("passport_office.interface.db.session_scope", return_value=mock_session):
            person_id = create_person["id"]
            sex_change_registration(person_id=person_id, new_sex="woman", date_of_change='2020-10-23')
            sex_change_record = mock_session.query(SexChange).filter_by(person_id=person_id).one_or_none()
            assert sex_change_record is not None
            assert sex_change_record.person_id == person_id
            assert sex_change_record.date_of_change.strftime("%Y-%m-%d") == '2020-10-23'


class TestBirthRegistration:
    def test_birt_registration(self, mock_session, marriage_registration):
        with patch("passport_office.interface.db.session_scope", return_value=mock_session):
            marriage = marriage_registration
            child_data = {'name': 'Dima',
                          'last_name': 'Shevchenko',
                          'middle_name': 'Fedorovich',
                          'date_of_birth': '2022-09-11',
                          'sex': 'man'}
            birth_registration(father_id=marriage["husband_id"], mother_id=marriage["wife_id"], date_of_birth="2022-09-11",
                               child_data=child_data)

            birth_data = mock_session.query(Birth).filter_by(father_id=marriage["husband_id"], mother_id=marriage["wife_id"]).one_or_none()
            assert birth_data is not None
            assert birth_data.father_id == marriage["husband_id"]
            assert birth_data.mother_id == marriage["wife_id"]
            assert birth_data.child.name == child_data['name']
            assert birth_data.child.last_name == child_data['last_name']
            assert birth_data.child.middle_name == child_data['middle_name']

            assert birth_data.date_of_birth.strftime("%Y-%m-%d") == '2022-09-11'


class TestAdoptionRegistration:
    def test_adoption(self, mock_session, marriage_registration, create_person):
        with patch("passport_office.interface.db.session_scope", return_value=mock_session):
            adoptive_child_id = create_person["id"]
            marriage = marriage_registration
            adoption_registration(father_id=marriage["husband_id"], mother_id=marriage["wife_id"], child_id=adoptive_child_id,
                                  date_of_adopt="2023-12-9")

            adoption = mock_session.query(Adoption).filter_by(adoptive_father_id=marriage["husband_id"],
                                                              adoptive_mother_id=marriage["wife_id"],
                                                              adopted_child_id=adoptive_child_id).one_or_none()

            assert adoption is not None
            assert adoption.adopted_child_id == adoptive_child_id


class TestGetHistory:
    def test_get_history(self, marriage_registration, mock_session):
        with patch("passport_office.interface.db.session_scope", return_value=mock_session):

            person_id = marriage_registration["husband_id"]
            try:
                get_person_history(person_id)
            except AssertionError as e:
                print(e.__str__())
















