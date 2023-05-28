from __future__ import annotations

import datetime
import json
import pathlib
from pathlib import Path
from abc import ABC, abstractmethod

from passport_db.db import PassportDB

from passport_office.models import Person

db = PassportDB()


class Context:

    def __init__(self, person_id, level):
        self._strategy = None
        self.person_id = person_id
        self.level = level

    @property
    def strategy(self) -> Strategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: Strategy) -> None:
        self._strategy = strategy

    def do_some_business_logic(self,) -> None:
        print(f"Context: Saving data via {self.__repr__()}")
        self._strategy.do_algorithm(
            json=f'{self.person_id}.json',
            json_to_save=f'{self.person_id}-clear.json',
            person_id = self.person_id,
            level = self.level

        )

    def __repr__(self):
        if "JSONStrategy" in str(self._strategy):
            return "JSONStrategy"

        elif "XMLStrategy" in str(self._strategy):
            return "XMLStrategy"


class Strategy(ABC):
    @abstractmethod
    def do_algorithm(self, **kwargs):
        pass

    @staticmethod
    def json_load(**kwargs):
        with open(kwargs.get("json"), "r") as json_file:
            json_dict = json.load(json_file)
        return json_dict


class JSONStrategy(Strategy):
    def do_algorithm(self, **kwargs: str) -> None:
        with open(kwargs.get("json_to_save"), "w") as json_file_to_save:
            pre_json_data = self.json_load(**kwargs)
            data = {}
            with db.session_scope() as session:
                data.update({'grand mother by father': pre_json_data.get("produce_3th_gen_ancestors"). \
                            get("grand_mother_by_father", 'No Data about grand mother'),
                             'grand father by father': pre_json_data.get("produce_3th_gen_ancestors"). \
                            get("grand_father_by_father", 'No Data about grand father'),
                             "grand mother by mother": pre_json_data.get("produce_3th_gen_ancestors"). \
                            get("grand_mother_by_mother", 'No Data about grand mother'),
                             'grand father by mother': pre_json_data.get("produce_3th_gen_ancestors"). \
                            get("grand_father_by_mother", 'No Data about grand father'),
                             'mother': pre_json_data.get("produce_2th_gen_ancestors"). \
                            get("mother", 'No Data about mother'),
                             'father': pre_json_data.get("produce_2th_gen_ancestors"). \
                            get("father", 'No Data about father'),
                             'brothers:': pre_json_data.get("produce_1th_gen_ancestors").\
                            get("brother", 'No Data about brother'),
                             'sisters': pre_json_data.get("produce_1th_gen_ancestors").\
                            get("sister", "No Data about sisters"),
                             'person': {key:str(value) if isinstance(value, datetime.date) else value for (key, value) in session.query(Person).\
                            filter_by(id = kwargs.get("person_id")).one().__dict__.items() if key != '_sa_instance_state'},
                             'children/grand children:': pre_json_data.\
                            get("children_and_grandchildren", "No Data about children/ grand children")})
            json.dump(data, json_file_to_save, indent=3)


class PrintStrategy(Strategy):

    def man_check(self, person, person_id):
        return (person.sex == 'man' and person_id == person.birth.father.id) or (
                    person.marriage.wife_id == person.birth.mother.id)

    def women_check(self, person, person_id):
        return (person.sex == 'women' and person_id == person.birth.mother.id) or (
                person.marriage.husband_id == person.birth.father.id)

    def do_algorithm(self, **kwargs: str) -> None:

        person_id = kwargs['person_id']

        def recurse_children(person, depth):
            if depth > kwargs['level'] or person is None: return
            print(" " * (4 * depth) + person.name)
            for child in person.children:
                recurse_children(child.person, depth + 1)

        def recurse_parents(person, depth):
            if depth > kwargs['level'] or person is None: return
            print(" " * (4 * depth) + person.name)
            parents = [person.birth.father, person.birth.mother]
            for parent_person in parents:
                if parent_person.sex == 'man':
                    if person.id == parents[0].id or person.marriage.husband_id == parent_person.id:
                        parent_person = None
                else:
                    if person.id == parents[1].id or person.marriage.wife_id == parent_person.id:
                        parent_person = None

                recurse_parents(parent_person, depth + 1)

        with db.session_scope() as session:
            person = session.query(Person).filter_by(id=person_id).one()
            mother_and_father = [person.birth.mother, person.birth.father] if person.birth is not None else []
            for p in mother_and_father:
                if self.man_check(p, person_id):
                    p = None
                elif self.women_check(p, person_id):
                    p = None
                recurse_parents(p, 0)

            recurse_children(person, 0)


