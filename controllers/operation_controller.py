from peewee import Model
from typing import Self
from datetime import datetime
import json

from database.models import Cinemas, Halls, Sessions


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

    @classmethod
    def de_db(cls, o):
        return cls(db_cls=Model, data=o.__dict__)

    @property
    def db(self):
        d = self.__dict__
        del d["db_cls"]
        del d["o_id"]
        return Cinemas.get_or_create(**d)

    def drop(self):
        self.db.delete_by_id(self.o_id)

    def __str__(self) -> str:
        raise NotImplemented("not implemented yet.")


class CinemaOC(BaseOperationController):
    @classmethod
    def create(cls) -> Self:
        data = {"name": input("Введите название кинотеатра: ")}

        return cls(db_cls=Cinemas, data=data)

    def __str__(self) -> str:
        return (
            "КИНОТЕАТР {}"
            "\nЗАЛЫ:"
            "{}".format(
            self.name, None
        ))


class HallOC(BaseOperationController):
    @classmethod
    def create(cls) -> Self:
        data = {
            "cinema": Cinemas.delete_by_id(int(input("Введите ID кинотеатра, к которому будет прикреплен зал: ")))
        }
        n, m = map(int, input("Введите размер зала в формате NxN где N - целое положительное число: ").split("x"))
        data["config_json"] = json.dumps([[False for _ in range(n)] for _ in range(m)])

        return cls(db_cls=Halls, data=data)

    def __str__(self) -> str:
        return (
            "ЗАЛ ID={}"
            "\nБлижайшие сеансы: {}".format(
                self.db.ID,
                map(str, map(SessionOC.de_db, Sessions.select().order_by(Sessions.starts_at).desc().limit(3)))
        ))


class SessionOC(BaseOperationController):
    @classmethod
    def create(cls) -> Self:
        data = {
            "film_name": input("Введите название фильма: "),
            "starts_at": datetime.strptime(
                input("Введите дату и время начала в формате дд/мм/гггг чч:мм: "), "%d/%m/%Y %HH:%MM"
            ),
            "duration": int(input("Введите длительность фильма (мин): ")),
            "hall": Halls.get(int(input("Введите ID зала, в котором будет проведен сеанс: ")))
        }

        return cls(db_cls=Sessions, data=data)

    @classmethod
    def de_db(cls, o):
        return cls(db_cls=Sessions, data=o.__dict__)

    def __str__(self) -> str:
        d = self.__dict__
        del d["o_id"]
        del d["db_cls"]
        del d["hall"]

        return (
            "СЕАНС НА ФИЛЬМ {}"
            "\nВремя начала: {}"
            "\nДлительность: {}".format(
                *d.values()
        ))
