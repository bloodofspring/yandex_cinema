from peewee import Model
from typing import Self, Any
from datetime import datetime
import json

from database.models import Cinemas, Halls, Sessions


class BaseOperationController:
    def __init__(self, m_type: type[Model], model: Model, data: dict[str, Any] | None = None) -> None:
        self.type = m_type
        self.model = model

        for k, v in zip(data.keys(), data.values()):
            self.__dict__[k] = v

        del self.__dict__['_dirty']
        del self.__dict__['__rel__']

    def __call__(self, *args, **kwargs):
        return type(self)(*args, **kwargs)

    def get(self, o_id: int | None = None) -> Self:
        model = self.type.get_by_id(o_id)
        return self(m_type=self.type, model=model, data=model.__dict__)

    @property
    def db(self):
        return self.model

    def drop(self):
        self.type.delete_by_id(self.model.ID)

    @classmethod
    def new(cls) -> Self:
        raise NotImplemented("not implemented yet.")

    def __str__(self) -> str:
        raise NotImplemented("not implemented yet.")


class SessionOC(BaseOperationController):
    def __init__(self, model: Model, data=None, **_):
        if data is None:
            data = self.__dict__
        super().__init__(m_type=Sessions, model=model, data=data)

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

        return cls(model=new, data=new.__dict__)

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


class HallOC(BaseOperationController):
    def __init__(self, model: Model, data=None, **_):
        if data is None:
            data = self.__dict__
        super().__init__(m_type=Halls, model=model, data=data)

    @classmethod
    def new(cls) -> Self:
        data = {
            "cinema": Cinemas.delete_by_id(int(input("Введите ID кинотеатра, к которому будет прикреплен зал: ")))
        }
        n, m = map(int, input("Введите размер зала в формате NxN где N - целое положительное число: ").split("x"))
        data["config_json"] = json.dumps([[False for _ in range(n)] for _ in range(m)])
        new = Halls.create(**data)

        return cls(model=new, data=new.__dict__)

    def __str__(self) -> str:
        return (
            "ЗАЛ ID={}"
            "\nБлижайшие сеансы: {}".format(
                self.db.ID,
                "\n".join(map(str, map(SessionOC.get, map(lambda x: x.ID, Sessions.select().order_by(Sessions.starts_at).limit(3)))))
        ))


class CinemaOC(BaseOperationController):
    def __init__(self, model: Model, data=None, **_):
        if data is None:
            data = self.__dict__
        super().__init__(m_type=Cinemas, model=model, data=data)

    @classmethod
    def new(cls):
        data = {"name": input("Введите название кинотеатра: ")}
        new = Cinemas.create(**data)

        return cls(model=new, data=new.__dict__)

    def __str__(self) -> str:
        return (
            "КИНОТЕАТР {}"
            "\nЗАЛЫ:"
            "{}".format(
            self.model.name,
                "\n".join(map(str, map(Halls.get, map(lambda x: x.ID, self.model.halls))))
        ))
