from __future__ import annotations

import copy
import json
from abc import ABC, abstractmethod

from genealogy.genealogy import Person
from passport_db.db import PassportDB

db = PassportDB()


class Builder(ABC):
    """
    The Builder interface specifies methods for creating the different parts of
    the Product objects.
    """

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


class FamilyTreeBuilder(Builder):
    """
    The Concrete Builder classes follow the Builder interface and provide
    specific implementations of the building steps. Your program may have
    several variations of Builders, implemented differently.
    """

    def __init__(self, person_id) -> None:
        """
        A fresh builder instance should contain a blank product object, which is
        used in further assembly.
        """
        self.person_id = person_id
        self.reset()

    def reset(self) -> None:
        self._product = GenealogyFile(self.person_id)

    @property
    def product(self):
        product = self._product
        return product

    @staticmethod
    def get_person_1th_generation(person_id):
        res = {}
        with db.session_scope() as session:
            target_person = session.query(Person).filter_by(id=person_id).one_or_none()
            brothers_and_sisters = target_person.birth.father.children
            for p in brothers_and_sisters:
                res.update({
                    'sex': p.person.sex,
                    'name': p.person.name,
                    'id': p.person.id,
                    'last_name': p.person.last_name,
                    'middle_name': p.person.middle_name,
                    'date_of_birth': p.person.date_of_birth}
                )
            return res

    @staticmethod
    def get_person_2th_generation(person_id):
        res = {}
        with db.session_scope() as session:
            target_person = session.query(Person).filter_by(id=person_id).one_or_none()
            parents = [target_person.birth.father, target_person.birth.mother]

            for p in parents:
                res.update({
                    'sex': p.person.sex,
                    'name': p.person.name,
                    'id': p.person.id,
                    'last_name': p.person.last_name,
                    'middle_name': p.person.middle_name,
                    'date_of_birth': p.person.date_of_birth}
                )
            return res

    @staticmethod
    def get_person_3th_generation(person_id):
        res = {}
        with db.session_scope() as session:
            target_person = session.query(Person).filter_by(id=person_id).one_or_none()
            grant_parents = [target_person.birth.father.birth.father, target_person.birth.mother.birth.mother]
            for p in grant_parents:
                res.update({
                    'sex': p.person.sex,
                    'name': p.person.name,
                    'id': p.person.id,
                    'last_name': p.person.last_name,
                    'middle_name': p.person.middle_name,
                    'date_of_birth': p.person.date_of_birth}
                )
            return res

    def produce_1th_gen_ancestors(self) -> None:
        with self._product as genealogy_file:
            res = self.get_person_1th_generation(self.person_id)
            json.dump({'produce_1th_gen_ancestors': res}, genealogy_file)

    def produce_2th_gen_ancestors(self) -> None:
        with self._product as genealogy_file:
            res = self.get_person_2th_generation(self.person_id)
            json.dump({'produce_2th_gen_ancestors': res}, genealogy_file)

    def produce_3th_gen_ancestors(self) -> None:
        with self._product as genealogy_file:
            res = self.get_person_3th_generation(self.person_id)
            json.dump({'produce_3th_gen_ancestors': res}, genealogy_file)


class GenealogyFile():
    """
    It makes sense to use the Builder pattern only when your products are quite
    complex and require extensive configuration.

    Unlike in other creational patterns, different concrete builders can produce
    unrelated products. In other words, results of various builders may not
    always follow the same interface.
    """

    def __init__(self, person_id) -> None:
        self.file_obj = open(f'{person_id}.json', 'w')

    def __enter__(self):
        return self.file_obj

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file_obj.close()


class Director:
    """
    The Director is only responsible for executing the building steps in a
    particular sequence. It is helpful when producing products according to a
    specific order or configuration. Strictly speaking, the Director class is
    optional, since the client can control builders directly.
    """

    def __init__(self, generation_count=None) -> None:
        self._builder = None
        self.generation_count = generation_count

    @property
    def builder(self) -> Builder:
        return self._builder

    @builder.setter
    def builder(self, builder: Builder) -> None:
        """
        The Director works with any builder instance that the client code passes
        to it. This way, the client code may alter the final type of the newly
        assembled product.
        """
        self._builder = builder

    """
    The Director can construct several product variations using the same
    building steps.
    """

    def build_generation_level(self) -> None:
        func_list = [self.builder.produce_1th_gen_ancestors,
                        self.builder.produce_2th_gen_ancestors,
                        self.builder.produce_3th_gen_ancestors]

        if self.generation_count is not None:
            count = len(func_list)
            func_list = copy.deepcopy(func_list[:count])

        for func in func_list:
            func()