from peewee import CharField, ForeignKeyField

from database.models.base import BaseModel


class Cinemas(BaseModel):
    name = CharField()


class Halls(BaseModel):
    config_json = CharField()
    cinema = ForeignKeyField(Cinemas, backref="halls")
