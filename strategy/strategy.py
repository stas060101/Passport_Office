from __future__ import annotations

import json
from abc import ABC, abstractmethod

import xmltodict

from passport_office.config import JSON_PATH, JSON_PATH_TO_SAVE, XML_PATH_TO_SAVE


class Context:

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
            json=JSON_PATH,
            json_to_save=JSON_PATH_TO_SAVE,
            xml_to_save=XML_PATH_TO_SAVE
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
            json.dump(JSONStrategy.json_load(**kwargs), json_file_to_save, indent=3)


class XMLStrategy(Strategy):
    def do_algorithm(self, **kwargs: str) -> None:
        with open(kwargs.get("xml_to_save"), "w") as xml_file:
            xmltodict.unparse(XMLStrategy.json_load(**kwargs), output=xml_file, pretty=True)


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
