from peewee import Model, DoesNotExist
from typing import Any, Self
from datetime import datetime
import json

from database.models import Cinemas, Halls


class CreateCinemaAsk(BaseAsk):
    @classmethod
    def generate(cls) -> Self:
        data = {}
        data["name"] = input("Введите название кинотеатра: ")

        return cls(data=data)


class CreateHall(BaseAsk):
    @classmethod
    def generate(cls) -> Self:
        data = {}
        data["cinema"] = Cinemas.delete_by_id(int(input("Введите ID кинотеатра, к которому будет прикреплен зал: ")))
        n, m = map(int, input("Введите размер зала в формате NxN где N - целое положительное число: ").split("x"))
        data["config_json"] = json.dumps([[False for _ in range(n)] for _ in range(m)])

        return cls(data=data)


class CreateSession(BaseAsk):
    @classmethod
    def generate(cls) -> Self:
        data = {}
        data["film_name"] = input("Введите название фильма: ")
        data["starts_at"] = datetime.strptime(
            input("Введите дату и время начала в формате дд/мм/гггг чч:мм: "), "%d/%m/%Y %HH:%MM"
        )
        data["duration"] = int(input("Введите длительность фильма (мин): "))
        data["hall"] = Halls.get(int(input("Введите ID зала, в котором будет проведен сеанс: ")))

        return cls(data=data)


class BaseOperationController:
    def __init__(self, db_cls: type[Model], o_id: int = -1, data=None):
        self.db_cls = db_cls
        self.o_id = o_id
        for k, v in data:
            self.__dict__[k] = v

    def __getitem__(self, item: int):
        return self.db_cls.get_by_id(item)

    @classmethod
    def create(cls) -> Self:
        # data = {}
        #
        # return cls(db_cls=Model, data=data)
        raise NotImplemented("not implemented yet.")

    @property
    def db(self):
        d = self.__dict__
        del d["db_cls"]
        del d["o_id"]
        return Cinemas.get_or_create(**d)

    def drop(self):
        self.db.delete_by_id(self.o_id)

    def config_about(self) -> str:
        raise NotImplemented("not implemented yet.")


class CinemaOC(BaseOperationController):
    @classmethod
    def create(cls) -> Self:
        data = {"name": input("Введите название кинотеатра: ")}

        return cls(db_cls=Cinemas, data=data)

    def config_about(self) -> str:
        return (
            "КИНОТЕАТР {}"
            "\nЗАЛЫ:"
            "{}".format(
            None, None
        ))
