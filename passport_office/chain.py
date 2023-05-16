from abc import ABC, abstractmethod
from datetime import datetime

from passport_office.models import Person


class Check(ABC):
    @abstractmethod
    def set_next(self, check):
        pass

    @abstractmethod
    def check(self, db=None,data=None, sex=None, person_ids =None, marriage_id=None):
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
            return self._next_check.check(data=data, sex=sex, person_ids=person_ids, marriage_id=marriage_id)


class DataCheck(AbstractCheck):
    def check(self, db=None, data=None, sex=None, person_ids=None, marriage_id=None):
        try:
            data_obj = self.data_convert(data)
        except:
            raise Exception()

        super().check(db=db, sex=sex, person_ids=person_ids, marriage_id=None)


class SexCheck(AbstractCheck):
    def check(self, db=None, data=None, sex=None, person_ids=None, marriage_id=None):
        gender = ['men', 'women']
        if sex not in gender:
            raise Exception
        else:
            print('successfully validation')
            super().check(db=db, person_ids=person_ids)


class PersonCheck(AbstractCheck):
    def check(self, db=None, data=None, sex=None, person_ids=None, marriage_id=None):
        with db.session_scope() as session:
            for id in person_ids:
                person_id = session.query(Person).filter_by(id=id).one_or_none()
                if person_id is None:
                    raise Exception

            print('successfully validation')


class MarriageCheck(AbstractCheck):
    def check(self, db=None, data=None, sex=None, person_ids=None, marriage_id=None):
        with db.session_scope() as session:
            person_id = session.query(Person).filter_by(id=marriage_id).one_or_none()
            if person_id is None:
                raise Exception

            print('successfully validation')

