from argparse import ArgumentParser, Namespace


def main():
    parser = ArgumentParser()

    # for operations
    opertions = parser.add_argument_group('Operations')
    opertions.add_argument('-o', '--object', help="Объект", type=str)

    options = parser.add_argument_group('Options')
    options.add_argument('-c', '--create', help="Создать экземпляр объекта (передавать ничего не надо)")
    options.add_argument('-a', '--about', help="Информация об объекте (передавать ничего не надо)")
    options.add_argument('-d', '--drop', help="Удалить объект (передавать ничего не надо)")

    # for "customers"
    parser.add_argument('-b', '--buy', help="Купить билет (передавать ничего не надо)")

    # for analytics
    analytics = parser.add_argument_group("Analytics")
    analytics.add_argument('-s', '--schedule', help="Расписание фильмов в .docx (передавать ничего не надо)")
    analytics.add_argument('-wl', '--workload', help="Загруженность в .xlsx (передавать ничего не надо)")
    analytics.add_argument('-ads', '--advertising', help="Реклама в .pptx (передавать ничего не надо)")

    args: Namespace = parser.parse_args()


if __name__ == "__main__":
    main()
