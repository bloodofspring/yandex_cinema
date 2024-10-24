from peewee import ForeignKeyField

from database.models import Sessions
from database.models.base import BaseModel


class SoldTickets(BaseModel):
    session = ForeignKeyField(Sessions, backref="sold_tickets")
