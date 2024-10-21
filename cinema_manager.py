from argparse import ArgumentParser, Namespace


def main():
    parser = ArgumentParser()

    # for operations

    parser.add_argument('-o', help="Объект", type=str)
    parser.add_argument('-c', '--create', help="Создать экземпляр объекта (передавать ничего не надо)")
    parser.add_argument('-a', '--about', help="Информация об объекте (передавать ничего не надо)")
    parser.add_argument('-d', '--drop', help="Удалить объект (передавать ничего не надо)")

    # for "customers"
    parser.add_argument('-b', '--buy', help="Купить билет (передавать ничего не надо)")

    # for analytics
    parser.add_argument('-s', '--schedule', help="Расписание фильмов в .docx (передавать ничего не надо)")
    parser.add_argument('-w', '--workload', help="Загруженность в .xlsx (передавать ничего не надо)")
    parser.add_argument('-a', '--advertising', help="Реклама в .pptx (передавать ничего не надо)")


if __name__ == "__main__":
    pass
