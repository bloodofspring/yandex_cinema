import json
from datetime import datetime

from database.models import Sessions, Halls, SoldTickets
from exceptions import FilmIsNotInCinema, PlaceIsTaken


class BuyController:
    def __init__(self):
        self.film_name = input("На сеанс какого фильма вы хотите приобрести билет? >> ")

    def load_data(self):
        available = tuple(filter(
            lambda r: any(list(map(lambda p: True in p, json.loads(r['hall'].config_json)))),
            map(
                lambda x: {'session': x, 'hall': x.hall, 'cinema': x.hall.cinema},
                Sessions.select().where(
                    (Sessions.film_name == self.film_name.strip()) & (Sessions.starts_at >= datetime.now())
                ).order_by(Sessions.starts_at)
            )
        ))

        return available

    def check_data(self, data):
        try:
            if not data:
                raise FilmIsNotInCinema(
                    f"Фильм {self.film_name} не идет в нашей сети кинотеатров или все места на него распроданы!"
                )

            cinema = self.load_hall(data=data)

            conf = json.loads(cinema['hall'].config_json)
            ypos = int(input("Введите ряд, на котором хотите сидеть: [int] >> ")) - 1
            xpos = int(input("Введите место, на котором хотите сидеть: [int] >> ")) - 1
            if not conf[ypos][xpos]:
                raise PlaceIsTaken("Это место уже занято!")

            self.finalize_buy(conf=conf, cinema=cinema, xpos=xpos, ypos=ypos)

        except (FilmIsNotInCinema, PlaceIsTaken) as err_message:
            print(err_message)

        except ValueError:
            print("Указано название несуществующего кинотеатра!")

        except IndexError:
            print("Указаны неверные координаты!")

    @staticmethod
    def load_hall(data):
        if len(data) != 1:
            print(f"Доступны кинотеатры: {', '.join(map(lambda x: x['cinema'].name, data))}")
            cinema = max(
                data,
                key=lambda x: x['cinema'].name == input(
                    "Введите название кинотеатра, в котором хотите купить билет: "
                )
            )
        else:
            cinema = data[0]

        cin_hall = '\n'.join(map(lambda r: ''.join(
            map(lambda p: '[{}]'.format('x' if not p else " "), r)
        ), json.loads(cinema['hall'].config_json)))
        row_len = len(json.loads(cinema['hall'].config_json)[0])

        print("Зал ([ ] - свободные места | [x] - занятые места):")
        print(f"/{'-' * row_len}ЭКРАН{'-' * row_len}\\")
        print(cin_hall)

        return cinema

    @staticmethod
    def log_transaction(session: Sessions):
        SoldTickets.create(session=session)

    def finalize_buy(self, conf, cinema, xpos, ypos):
        self.log_transaction(session=cinema["session"])
        conf[ypos][xpos] = False
        cinema['hall'].config_json = json.dumps(conf)
        Halls.save(cinema['hall'])
        print(f"Приобретен билет на сеанс в кинотеатре {cinema['cinema'].name} на {self.film_name}!")
        print(f"Ряд {ypos + 1} место {xpos + 1}")

    def __call__(self):
        self.check_data(data=self.load_data())
