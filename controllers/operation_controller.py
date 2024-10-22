from peewee import Model
from controllers.ask_functions import BaseAsk


class OperationController:
    def __init__(self, cls: Model, obj_id: int | None = None):
        self.cls: Model = cls
        self.obj: Model | None = self.get_obj(obj_id ) if obj_id is not None else None

    def get_obj(self, obj_id: int):
        return self.cls.get_by_id(obj_id)

    def create(self, ask_f: BaseAsk | None = None, **kwargs):
        if ask_f:
            kwargs = ask_f.generate()

        self.obj.create(**kwargs.to_dict)

    def drop(self):
        self.obj.delete_by_id(self.obj.ID)

    def config_about(self, sample: str):
        pass
