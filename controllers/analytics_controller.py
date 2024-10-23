from datetime import datetime

from matplotlib import pyplot

from controllers.operation_controller import CinemaOC


class AnalyticsController:
    def buy_stats(self) -> str:
        cinema = CinemaOC.get(int(input("Введите ID кинотеатра: ")))
        pyplot.title(f"Загруженность кинотеатра {cinema.name}")
        pyplot.ylabel("Количество купленных билетов")
        pyplot.plot_date(map(lambda x: x, []))

        name = f"{cinema.name}_analytics_{str(datetime.now()).replace(' ', '_')}"
        pyplot.savefig(f"{cinema.name}")

        return name  # Вернуть имя фала с графиком

    def ads_pptx(self) -> str:
        return "" # Вернуть имя фала с презентацией
