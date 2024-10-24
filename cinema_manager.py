from argparse import ArgumentParser, Namespace
from database import create_tables

from controllers import Controller


def main():
    create_tables()

    parser = ArgumentParser()

    # for operations
    opertions = parser.add_argument_group('Operations')
    opertions.add_argument('-o', '--object', help="Объект [cinema/hall/session]", type=str)

    options = parser.add_argument_group('Options')
    options.add_argument('-c', '--create', help="Создать экземпляр объекта")
    options.add_argument('-a', '--about', help="Информация об объекте")
    options.add_argument('-d', '--drop', help="Удалить объект")

    # for "customers"
    parser.add_argument('-b', '--buy', help="Купить билет")

    # for analytics
    analytics = parser.add_argument_group("Analytics")
    analytics.add_argument('-wl', '--workload', help="Загруженность (график)")
    analytics.add_argument('-ads', '--advertising', help="РГрафик сеансов (coming in the next update)")

    args: Namespace = parser.parse_args()
    Controller(args=args).execute_cmd()


if __name__ == "__main__":
    main()
