import json
from datetime import datetime
from typing import Self, Any

from peewee import Model

from database.models import Cinemas, Halls, Sessions


class BaseOperationController:
    type: Model | None = None

    def __init__(self, model: Model, data: dict[str, Any] | None = None) -> None:
        self.model = model

        for k in data:
            setattr(self, k, data[k])

    def __call__(self, *args, **kwargs):
        return type(self)(*args, **kwargs)

    @classmethod
    def get(cls, o_id: int | None = None) -> Self:
        model = cls.type.get_by_id(o_id)
        return cls(model=model, data=model.__dict__["__data__"])

    @property
    def db(self):
        return self.model

    def drop(self):
        self.type.delete_by_id(self.ID)

    @classmethod
    def new(cls) -> Self:
        raise NotImplemented("not implemented yet.")

    def __str__(self) -> str:
        raise NotImplemented("not implemented yet.")

    def __eq__(self, other: Model):
        return self.model == other


class SessionOC(BaseOperationController):
    type = Sessions

    @classmethod
    def new(cls) -> Self:
        data = {
            "film_name": input("Введите название фильма: "),
            "starts_at": datetime.strptime(
                input("Введите дату и время начала в формате дд/мм/гггг чч:мм: "), "%d/%m/%Y %H:%M"
            ),
            "duration": int(input("Введите длительность фильма (мин): ")),
            "hall": Halls.get(int(input("Введите ID зала, в котором будет проведен сеанс: ")))
        }
        new = Sessions.create(**data)

        return cls(model=new, data=new.__dict__.get("__data__"))

    def __str__(self) -> str:
        return (
            "СЕАНС НА ФИЛЬМ {}"
            "\nВремя начала: {}"
            "\nДлительность: {} минут"
            "\nID зала: {}".format(
                self.film_name, self.starts_at, self.duration, Halls(ID=self.hall).ID
            ))


class HallOC(BaseOperationController):
    type = Halls

    @classmethod
    def new(cls) -> Self:
        data = {
            "cinema": Cinemas.delete_by_id(int(input("Введите ID кинотеатра, к которому будет прикреплен зал: ")))
        }
        n, m = map(int, input("Введите размер зала в формате NxN где N - целое положительное число: ").split("x"))
        data["config_json"] = json.dumps([[False for _ in range(n)] for _ in range(m)])
        new = Halls.create(**data)

        return cls(model=new, data=new.__dict__.get("__data__"))

    def __str__(self) -> str:
        now = datetime.now()
        near_sessions = "\n".join(map(str, map(SessionOC.get, map(
            lambda x: x.ID,
            Sessions.select().where(self == Sessions.hall & Sessions.starts_at >= now).order_by(
                Sessions.starts_at).limit(3)
        ))))
        if not near_sessions:
            near_sessions = f"В зале {self.ID} не запланировано сеансов!"

        return (
            "ЗАЛ ID={}"
            "\nБлижайшие сеансы: {}".format(
                self.db.ID,
                near_sessions
            ))


class CinemaOC(BaseOperationController):
    type = Cinemas

    @classmethod
    def new(cls):
        data = {"name": input("Введите название кинотеатра: ")}
        new = Cinemas.create(**data)

        return cls(model=new, data=new.__dict__.get("__data__"))

    def __str__(self) -> str:
        halls = "\n".join(map(str, map(Halls.get, map(lambda x: x.ID, self.model.halls))))
        if not halls:
            halls = "В кинотеатре нет залов!"

        return (
            "КИНОТЕАТР {}"
            "\nЗАЛЫ: "
            "{}".format(
                self.name, halls,
            ))
