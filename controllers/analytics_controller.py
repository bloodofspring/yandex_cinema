from datetime import datetime

from matplotlib import pyplot
from numpy import array
import itertools

from controllers.operation_controller import CinemaOC, SessionOC


class GotData:
    def __init__(self, cinema: CinemaOC, sessions: list[SessionOC]):
        self.sessions = sessions
        self.cinema = cinema


class AnalyticsController:
    @staticmethod
    def get_data() -> GotData:
        cin = CinemaOC.get(int(input("Введите ID кинотеатра для построения аналитики: ")))
        sessions = list(itertools.chain(map(lambda x: x.sessions, cin.model.halls)))
        return GotData(cinema=cin, sessions=sessions)

    def buy_stats(self) -> str:
        d = self.get_data()
        an_data = d.sessions[-50:]

        pyplot.title(f"Загруженность кинотеатра {d.cinema.name}")
        pyplot.ylabel("Количество купленных билетов")
        pyplot.xlabel(f"День (1: {an_data[0].sold_tickets} -> {len(an_data)}: {an_data[-1].sold_tickets})")
        pyplot.minorticks_on()
        pyplot.grid(visible=True)

        arr = array(an_data)
        pyplot.plot(arr, color="black")

        name = f"{d.cinema.name}_analytics_{str(datetime.now()).replace(' ', '_').replace('.', '')}"
        pyplot.savefig(name)

        return name  # Вернуть имя фала с графиком

    def ads_pptx(self) -> str:
        return "" # Вернуть имя фала с презентацией
