from argparse import Namespace


class Controller:
    def __init__(self, args: Namespace):
        self.args = args
        self.cases()

    def cases(self):
        match self.args:
            case _ as c if c.object is not None:
                pass

            case _ as c if c.buy is not None:
                pass

            case _ as c if c.schedule is not None:
                pass

    def execute_operation(self):
        pass

    def buy(self):
        pass

    def analytics(self):
        pass
