from __future__ import annotations

import json
import os
from abc import ABC, abstractmethod

import xmltodict


class Context:
    json_path = 'files/json.json'
    json_path_to_save = f'/home/{os.environ.get("USER")}/PycharmProjects/Passport_Office/strategy/files/json_saved.json'
    xml_path_to_save = f'/home/{os.environ.get("USER")}/PycharmProjects/Passport_Office/strategy/files/xml_saved.xml'

    def __init__(self, strategy: Strategy):
        self._strategy = strategy

    @property
    def strategy(self) -> Strategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: Strategy) -> None:
        self._strategy = strategy

    def do_some_business_logic(self) -> None:
        print(f"Context: Saving data via {self.__repr__()}")
        self._strategy.do_algorithm(
            json=self.json_path,
            json_to_save=self.json_path_to_save,
            xml_to_save=self.xml_path_to_save
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


class JSONStrategy(Strategy):
    def do_algorithm(self, **kwargs: str):
        with open(kwargs.get("json"), "r") as json_file:
            json_data = json.load(json_file)
        with open(kwargs.get("json_to_save"), "w") as json_file_to_save:
            json.dump(json_data, json_file_to_save, indent=3)


class XMLStrategy(Strategy):
    def do_algorithm(self, **kwargs: str):
        with open(kwargs.get("json"), "r") as json_file:
            python_dict = json.load(json_file)
        with open(kwargs.get("xml_to_save"), "w") as xml_file:
            xmltodict.unparse(python_dict, output=xml_file, pretty=True)


if __name__ == "__main__":
    while True:
        context = Context(JSONStrategy())
        input_type = input("Select JSON or XML: \n")

        if input_type == "json" or input_type == "JSON":
            print("Client: Strategy is set to json save.")
            context.strategy = JSONStrategy()
            context.do_some_business_logic()

        elif input_type == "xml" or input_type == "XML":
            print("Client: Strategy is set to xml save.")
            context.strategy = XMLStrategy()
            context.do_some_business_logic()

        else:
            print("Wrong input type of saving file")
