from peewee import CharField, DateTimeField, IntegerField, ForeignKeyField

from database.models.base import BaseModel
from database.models.cinemas import Halls


class Sessions(BaseModel):
    film_name = CharField()
    starts_at = DateTimeField()
    duration = IntegerField()  # in minutes
    hall = ForeignKeyField(Halls, backref="sessions")
