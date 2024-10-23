from peewee import ForeignKeyField, CharField

from database.models import Sessions
from database.models.base import BaseModel


class SoldTickets(BaseModel):
    session = ForeignKeyField(Sessions, backref="sold_tickets")


class Ads(BaseModel):
    file_name = CharField()
    film = ForeignKeyField(Sessions, backref="ads")
