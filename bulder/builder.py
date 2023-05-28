from __future__ import annotations

import collections
import copy
import json
from abc import ABC, abstractmethod

from  passport_office.models import Person
from passport_db.db import PassportDB

db = PassportDB()


class Builder(ABC):

    @property
    @abstractmethod
    def product(self) -> None:
        pass

    @abstractmethod
    def produce_1th_gen_ancestors(self) -> None:
        pass

    @abstractmethod
    def produce_2th_gen_ancestors(self) -> None:
        pass

    @abstractmethod
    def produce_3th_gen_ancestors(self) -> None:
        pass

    def write_result(self) -> None:
        pass


class FamilyTreeBuilder(Builder):

    def __init__(self, person_id) -> None:
        self.person_id = person_id
        self.reset()
        self.data = {}
        self.recursive_child = {}

    def reset(self) -> None:
        self._product = GenealogyFile(self.person_id)

    @property
    def product(self):
        product = self._product
        return product

    def get_person_1th_generation(self, person_id):
        res = collections.defaultdict(list)

        with db.session_scope() as session:
            target_person = session.query(Person).filter_by(id=person_id).one_or_none()
            if target_person.children is not None or target_person.adoption is not None:
                children = target_person.children.extend(target_person.adoption)
                for child in children:
                    self.recursive_child.update({f'{target_person.name} - {child.person.name}': self.get_person_1th_generation(child.person.id)})

            if target_person.birth is not None:
                brothers_and_sisters = target_person.birth.father.children if target_person.sex == 'man' else target_person.birth.mother.children
                compared_value = target_person.birth.father.id if target_person.sex == 'man' else target_person.birth.mother.id
            else:
                brothers_and_sisters = []

            for p in brothers_and_sisters:
                if p.person.sex == 'man':
                    key = 'brother'
                    if target_person.id == compared_value:
                        value = 'No Data'
                    else:
                        value = None
                else:
                    key = 'sister'
                    if target_person.id == compared_value:
                        value = 'No Data'
                    else:
                        value = None
                res[key].append({
                    'sex': p.person.sex,
                    'name': p.person.name,
                    'id': p.person.id,
                    'last_name': p.person.last_name,
                    'middle_name': p.person.middle_name,
                    'date_of_birth': f'{p.person.date_of_birth}'}) if value is None else value

            return res

    def get_person_2th_generation(self, person_id):
        res = {}
        with db.session_scope() as session:
            target_person = session.query(Person).filter_by(id=person_id).one_or_none()
            parents = [target_person.birth.father if target_person.birth.father.id != target_person.id and
                                                     target_person.birth.father.id != (target_person.marriage.husband_id\
                                                                                           if target_person.marriage is not None else target_person.id) else None,
                       target_person.birth.mother if target_person.birth.mother.id != target_person.id and
                                                     target_person.birth.mother.id != (target_person.marriage.wife_id\
                                                                                           if target_person.marriage is not None else target_person.id) else None] \
            if target_person.birth is not None else []
            count = 1
            for p in parents:
                count = count
                if p is not None:
                    if p.sex == 'man':
                        key = 'father'

                    else :
                        key = 'mother'

                    res[key] = {
                        'sex': p.sex,
                        'name': p.name,
                        'id': p.id,
                        'last_name': p.last_name,
                        'middle_name': p.middle_name,
                        'date_of_birth': f'{p.date_of_birth}'}

                else:
                    if count == 1:
                        res['father'] = 'No data about father'
                    else:
                        res['mother'] = 'No data about mother'

                count +=1

            return res

    def get_person_3th_generation(self, person_id):
        res = {}
        with db.session_scope() as session:
            target_person = session.query(Person).filter_by(id=person_id).one_or_none()
            grant_parents = {"grand_father_by_father": target_person.birth.father.birth.father if target_person.birth.father.birth.father.id != target_person.birth.father.id
                and target_person.birth.father.birth.father.id != target_person.birth.father.marriage.husband_id else None,
                             "grand_mother_by_father": target_person.birth.father.birth.mother if target_person.birth.father.birth.mother.id != target_person.birth.mother.id
                and target_person.birth.father.birth.mother.id != target_person.birth.father.marriage.wife_id else None,
                             "grand_father_by_mother": target_person.birth.mother.birth.father if target_person.birth.mother.birth.father.id != target_person.birth.father.id
                and target_person.birth.mother.birth.father.id != target_person.birth.father.marriage.husband_id else None,
                             "grand_mother_by_mother":target_person.birth.mother.birth.mother if target_person.birth.mother.birth.mother.id != target_person.birth.mother.id
                and target_person.birth.mother.birth.mother != target_person.birth.father.marriage.wife_id else None} \
                if target_person.birth is not None else {"grand_father_by_father": None, "grand_mother_by_father": None,
                                                         "grand_father_by_mother": None, "grand_mother_by_mother": None}

            for key, p in grant_parents.items():
                if p is not None:
                    res.update({key: {
                        'sex': p.sex,
                        'name': p.name,
                        'id': p.id,
                        'last_name': p.last_name,
                        'middle_name': p.middle_name,
                        'date_of_birth': f'{p.date_of_birth}'}})
                else:
                    if key == "grand_father_by_father":
                        res.update({key: "No data about grand father by father"})
                    elif key == "grand_mother_by_father":
                        res.update({key: "No data about grand mother by father"})
                    elif key == "grand_father_by_mother":
                        res.update({key: "No data about grand father by mother"})
                    elif key == "grand_mother_by_mother":
                        res.update({key: "No data about grand mother by mother"})

            return res

    def produce_1th_gen_ancestors(self) -> None:
        res = self.get_person_1th_generation(self.person_id)
        self.data.update({'produce_1th_gen_ancestors': res})
        self.data.update({'children_and_grandchildren': self.recursive_child})

    def produce_2th_gen_ancestors(self) -> None:
        res = self.get_person_2th_generation(self.person_id)
        self.data.update({'produce_2th_gen_ancestors': res})

    def produce_3th_gen_ancestors(self) -> None:
        res = self.get_person_3th_generation(self.person_id)
        self.data.update({'produce_3th_gen_ancestors': res})

    def write_result(self):
        with self._product as genealogy_file:
            json.dump(self.data, genealogy_file, sort_keys=True, indent=4)


class GenealogyFile:

    def __init__(self, person_id) -> None:
        self.file_path = f'{person_id}.json'
        self.person_id = person_id

    def __enter__(self):
        self.file_obj = open(self.file_path, 'a')
        return self.file_obj

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file_obj.close()


class Director:

    def __init__(self, generation_count=None) -> None:
        self._builder = None
        self.generation_count = generation_count

    @property
    def builder(self) -> Builder:
        return self._builder

    @builder.setter
    def builder(self, builder: Builder) -> None:
        self._builder = builder

    def build_generation_level(self) -> None:
        func_list = [self.builder.produce_1th_gen_ancestors,
                        self.builder.produce_2th_gen_ancestors,
                        self.builder.produce_3th_gen_ancestors,
                        self.builder.write_result]

        if self.generation_count is not None:
            count = len(func_list)
            func_list = copy.deepcopy(func_list[:count])

        for func in func_list:
            func()