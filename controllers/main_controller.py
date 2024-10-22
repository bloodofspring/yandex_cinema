import os
from argparse import Namespace

from controllers.operation_controller import BaseOperationController, HallOC, CinemaOC, SessionOC


class Controller:
    def __init__(self, args: Namespace):
        self.args = args

    @staticmethod
    def clear_console(next_output: str = ""):
        os.system('cls' if os.name == 'nt' else 'clear')
        if next_output:
            print(next_output)

    def execute_cmd(self):
        match self.args:
            case _ as c if c.object is not None:
                self.execute_operation()

            case _ as c if c.buy is not None:
                self.buy()

            case _ as c if c.schedule is not None:
                self.analytics()

    def execute_operation(self):
        operator: BaseOperationController = {
            "cinema": CinemaOC,
            "hall": HallOC,
            "session": SessionOC
        }[self.args.object]

        if self.args.create:
            operator.new()
            self.clear_console(next_output=f"{self.args.object} created!")

        if self.args.about:
            o_id = int(input("Введите ID объекта: [int] >> "))
            self.clear_console(next_output=str(operator.get(o_id)))

        if self.args.drop:
            o_id = int(input("Введите ID объекта: [int] >> "))
            operator.get(o_id).drop()
            self.clear_console(next_output=f"{self.args.object} dropped!")

    def buy(self):
        pass

    def analytics(self):
        if self.args.schedule:
            pass

        if self.args.workload:
            pass

        if self.args.advertising:
            pass
