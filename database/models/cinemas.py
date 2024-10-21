from peewee import CharField

from database.models.base import BaseModel


class Cinemas(BaseModel):
    name = CharField()
