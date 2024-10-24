from collections.abc import Iterable
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
        sessions = list(itertools.chain(map(lambda x: x.sessions, cin.model.halls)))
        return GotData(cinema=cin, sessions=sessions)

    def build_pyplot(self, title: str, data: Iterable[int], file_name: str = "", xlabel: str = "", ylabel: str = "") -> str:
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

        pyplot.savefig(file_name)

        return file_name


    def buy_stats(self) -> str:
        d = self.get_data()
        build_data = d.sessions[-50:]

        return self.build_pyplot(
            title=f"Загруженность кинотеатра {d.cinema.name}",
            xlabel=f"День (1: {build_data[0].sold_tickets} -> {len(build_data)}: {build_data[-1].sold_tickets})",
            ylabel="Количество купленных билетов",
            data=map(lambda x: len(SoldTickets.select().where(SoldTickets.session == x)), build_data),
        )

    def session_stats(self) -> str:
        pass  # coming soon
