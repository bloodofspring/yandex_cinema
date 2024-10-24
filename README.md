# Yandex Cinema (beta)
### Терминальная система для менеджмента и аналитики сети кинотеатров

### Быстрый старт
Для начала работы необходимо перенести все данные в локальную сеть, т. е. создать сеть кинотеатров, залов и сеансов
Для этого необходимо воспользоваться командами:

* Создать кинотеатр
```commandline
python cinema_manager.py -o cinema -c pass
```

* Создать зал
```commandline
python cinema_manager.py -o hall -c pass
```

* Создать сеанс
```commandline
python cinema_manager.py -o session -c pass
```

После того, как ваша сеть будет создана и настроена, можно приступать к аналитике и покупке билетов
* Просмотреть статистику по купленным билетам
```commandline
python cinema_manager.py -wl pass
```

* Купить билет
```commandline
python cinema_manager.py -b pass
```


### Расширенные возможности и полная информация
```commandline
usage: cinema_manager.py [-h] [-o OBJECT] [-c CREATE] [-a ABOUT] [-d DROP] [-b BUY] [-wl WORKLOAD] [-ads ADVERTISING]

options:
  -h, --help            show this help message and exit
  -b, --buy BUY         Купить билет

Operations:
  -o, --object OBJECT   Объект [cinema/hall/session]

Options:
  -c, --create CREATE   Создать экземпляр объекта
  -a, --about ABOUT     Информация об объекте
  -d, --drop DROP       Удалить объект

Analytics:
  -wl, --workload WORKLOAD Загруженность (график)
  -ads, --advertising ADVERTISING Гррафик сеансов (coming in the next update)
```
