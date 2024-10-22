from argparse import Namespace


class Controller:
    def __init__(self, args: Namespace):
        self.args = args
        self.cases()

    def cases(self):
        match self.args:
            case _ as c if c.object is not None:
                self.execute_operation()

            case _ as c if c.buy is not None:
                self.buy()

            case _ as c if c.schedule is not None:
                self.analytics()

    def execute_operation(self):
        if self.args.create:
            pass

        if self.args.about:
            pass

        if self.args.drop:
            pass

    def buy(self):
        pass

    def analytics(self):
        if self.args.schedule:
            pass

        if self.args.workload:
            pass

        if self.args.advertising:
            pass
