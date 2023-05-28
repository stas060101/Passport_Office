from abc import ABC, abstractmethod
from datetime import datetime

from passport_office.models import Person, Marriage


class Check(ABC):
    @abstractmethod
    def set_next(self, check):
        pass

    @abstractmethod
    def check(self, db=None, data=None, sex=None, person_ids=None, marriage_id=None):
        pass

    @staticmethod
    def data_convert(data_str):
        date_format = '%Y-%m-%d'
        return datetime.strptime(data_str, date_format)


class AbstractCheck(Check):
    _next_check = None

    def set_next(self, check: Check):
        self._next_check = check
        return check

    @abstractmethod
    def check(self, db=None, data=None, sex=None, person_ids=None, marriage_id=None):
        if self._next_check:
            return self._next_check.check(db=db, data=data, sex=sex, person_ids=person_ids, marriage_id=marriage_id)


class DataCheck(AbstractCheck):
    def check(self, db=None, data=None, sex=None, person_ids=None, marriage_id=None):
        try:
            data_obj = self.data_convert(data)
        except:
            raise Exception("Data does not match with format 'YYYY-MM-DD'")
        print('successfully validation - data')
        super().check(db=db, sex=sex, person_ids=person_ids, marriage_id=marriage_id)


class SexCheck(AbstractCheck):
    def check(self, db=None, data=None, sex=None, person_ids=None, marriage_id=None):
        gender = ['man', 'woman']
        if sex not in gender:
            raise Exception("Sex does not match with allowed type. Must be 'man' or 'woman'")
        else:
            print('successfully validation - sex')
            super().check(db=db, person_ids=person_ids)


class PersonCheck(AbstractCheck):
    def check(self, db=None, data=None, sex=None, person_ids=None, marriage_id=None):
        with db.session_scope() as session:
            if len(person_ids) == 1:
                for id in person_ids:
                    person_id = session.query(Person).filter_by(id=id).one_or_none()
                    if person_id is None:
                        raise Exception('No person with this ID')

            elif len(person_ids) == 2:  # for marriage and genealogy(?)
                for id in person_ids:
                    person_id = session.query(Person).filter_by(id=id).one_or_none()
                    if person_id is None and person_ids.index(id) == 0:
                        raise Exception('No husband with this ID')
                    elif person_id is None and person_ids.index(id) == 1:
                        raise Exception('No wife with this ID')

            elif len(person_ids) == 3:  # for adoption and birth
                for id in person_ids:
                    person_id = session.query(Person).filter_by(id=id).one_or_none()
                    if person_id is None and person_ids.index(id) == 0:
                        raise Exception('No father with this ID')
                    elif person_id is None and person_ids.index(id) == 1:
                        raise Exception('No mother with this ID')
                    elif person_id is None and person_ids.index(id) == 2:
                        raise Exception('No child with this ID')

            print('successfully validation - person')
            super().check(db=db, person_ids=person_ids)


class MarriageCheck(AbstractCheck):
    def check(self, db=None, data=None, sex=None, person_ids=None, marriage_id=None):
        with db.session_scope() as session:
            marriage = session.query(Marriage).filter_by(id=marriage_id).one_or_none()
            if marriage is None:
                raise Exception('No marriage with this ID')

            print('successfully validation - marriage')


class MarriageCheckByPerson(AbstractCheck):
    def check(self, db=None, data=None, sex=None, person_ids=None, marriage_id=None):
        with db.session_scope() as session:
            marriage = session.query(Marriage).filter(Marriage.husband_id == person_ids[0], Marriage.wife_id ==
                                                      person_ids[1]).one_or_none()
            if marriage is None:
                raise Exception('No marriage with this persons')


