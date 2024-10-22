from typing import Any, Self
from datetime import datetime
import json

from database.models import Cinemas, Halls


class BaseAsk:
    def __init__(self, data: dict[str, Any]):
        for k, v in data:
            self.__dict__[k] = v

    @classmethod
    def generate(cls) -> Self:
        data = {}

        return cls(data=data)

    @property
    def to_dict(self):
        return self.__dict__


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
