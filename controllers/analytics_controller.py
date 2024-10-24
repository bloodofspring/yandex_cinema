import os.path
from datetime import datetime

from matplotlib import pyplot
from numpy import array
import itertools

from controllers.operation_controller import CinemaOC, SessionOC
from database.models import SoldTickets


class GotData:
    def __init__(self, cinema: CinemaOC, sessions: list[SessionOC]):
        self.sessions = sessions
        self.cinema = cinema


class AnalyticsController:
    def __init__(self):
        self.data = self.get_data()
        self.default_file_name = "{}_analytics_{}".format(
            self.data.cinema.name, str(datetime.now()).replace(' ', '_').replace('.', '')
        )

    @staticmethod
    def get_data() -> GotData:
        cin = CinemaOC.get(int(input("Введите ID кинотеатра для построения аналитики: ")))
        sessions = list(itertools.chain(*map(lambda x: x.sessions[:], cin.model.halls)))
        return GotData(cinema=cin, sessions=sessions)

    def build_pyplot(self, title: str, data: tuple, file_name: str = "", xlabel: str = "", ylabel: str = "") -> str:
        pyplot.title(title)

        if xlabel:
            pyplot.xlabel(xlabel)

        if ylabel:
            pyplot.ylabel(ylabel)

        pyplot.minorticks_on()
        pyplot.grid(visible=True)

        arr = array(data)
        pyplot.plot(arr, color="black")

        if not file_name:
            file_name = self.default_file_name

        if not os.path.exists("statistics"):
            os.mkdir("statistics")

        pyplot.savefig(f"statistics/{file_name}")

        return file_name


    def buy_stats(self) -> str:
        build_data = self.data.sessions[-50:]
        if not build_data:
            raise Exception("У данного кинотеатра нет залов!")

        return self.build_pyplot(
            title=f"Загруженность кинотеатра {self.data.cinema.name}",
            xlabel=(
                f"День 1: продано {len(build_data[0].sold_tickets)}  "
                ">>----->  "
                f"День {len(build_data)}: продано {len(build_data[-1].sold_tickets)}"
            ),
            ylabel="Количество купленных билетов",
            data=tuple(map(lambda x: len(SoldTickets.select().where(SoldTickets.session == x)), build_data)),
        )

    def session_stats(self) -> str:
        raise Exception("Данный метод будет реализован в следующей версии!")
