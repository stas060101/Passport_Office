import random
from uuid import uuid4

import factory
from passport_office import models
from unit_tests.common import Session


class PersonFactory(factory.alchemy.SQLAlchemyModelFactory):

    class Meta:
        model = models.Person
        sqlalchemy_session = Session

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Custom create method for not generating duplicates"""
        obj = model_class(*args, **kwargs)
        return obj

    @factory.post_generation
    def assign_id(obj, *args, **kwargs):
        obj.id = random.randint(1, 10)
        return obj


class MarriageFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Marriage
        sqlalchemy_session = Session

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Custom create method for not generating duplicates"""
        obj = model_class(*args, **kwargs)
        return obj

    @factory.post_generation
    def assign_id(obj, *args, **kwargs):
        obj.id = random.randint(1, 5)
        return obj






