import sys
from dataclasses import dataclass, asdict
from random import randint, uniform
from requests import get


# пользовательский класс исключений
class CountyNotInRangeError(Exception):
    def __init__(self, country, message="Такой страны производтва не существует"):
        self.country = country
        self.message = message

    # переопределяем метод '__str__'
    def __str__(self):
        return f'{self.country} -> {self.message}'

# Дата класс
@dataclass
class Fluid():
    """0) Жидкость"""
    temp: int  # [*] Температура
    amount: float  # [*] Объем

    # Свойства
    @property
    def name(self):  # [*] Название
        return self.__name

    @name.setter
    def name(self, name):
        if len(name) > 0:
            self.__name = name
        else:
            raise ValueError("Имя не может быть пустым")

    def __str__(self):
        return f'Жидкость "{self.name}" ({self.amount} л.) температура {self.temp}°'

    # Перегрузка арифметических операторов
    # Логично, что можно смешать любой напиток
    def __add__(self, other):  # +
        # Мы можем влить напиток в другой
        # т.е. получаем новую жидкость
        if issubclass(type(other), Fluid):
            t = Fluid((self.temp + other.temp) / 2, self.amount + other.amount)
            t.name = f"{self.name} + {other.name}"
            return t
        # Можем добавить еще 1 литр идентичной жидкости (миситика, но почему нет? )
        elif isinstance(other, int) or isinstance(other, float):
            self.amount += other
            return self
        else:
            raise TypeError(f"Нельзя складывать объекты типов {self.__class__} и {type(other)}")

    def __sub__(self, other):  # -
        if isinstance(other, int) or isinstance(other, float):
            self.amount -= other
            return self
        else:
            raise TypeError(f"Нельзя вычитать объекты типов {self.__class__} и {type(other)}")

    def __mul__(self, other):  # *
        if isinstance(other, int) or isinstance(other, float):
            self.amount *= other
            return self
        else:
            raise TypeError(f"Нельзя перемножать объекты типов {self.__class__} и {type(other)}")

    def __truediv__(self, other):  # /
        if isinstance(other, int) or isinstance(other, float):
            return self.amount * other.amount
        else:
            raise TypeError(f"Нельзя поделить объекты типов {self.__class__} и {type(other)}")


@dataclass
class Drink(Fluid):
    """1) Напиток"""
    sweet: bool  # Сладкий?
    sour: bool  # Кислый?
    structure: str  # Состав

    def get_sweet_or_sour(self):
        # Можно ли это как-то сократить?
        if self.sweet and self.sour:
            str = 'Кисло-сладкий'
        elif self.sweet:
            str = 'Сладкий'
        elif self.sour:
            str = 'Кислый'
        else:
            str = 'Нейтральный'

        return str

    def __str__(self):
        return f'{self.get_sweet_or_sour()} напиток "{self.name}" температура {self.temp}°, состав: "{self.structure}"'

    def __add__(self, other):  # +
        if isinstance(other, __class__):
            return Fluid(f"{self.name}", (self.temp + other.temp) / 2, self.amount + other.amount)
        elif isinstance(other, int) or isinstance(other, float):
            self.amount += other
            return self
        else:
            raise TypeError(f"Нельзя складывать объекты типов {self.__class__} и {type(other)}") 


class Tea(Drink):
    """
    2) Чай
        [0] Название
        [0] Температура
        [1] Сладкий?
        [1] Кислый?
        [1] Состав
        [*] Форма чая (Байховые [рассыпные],
                       Прессованные [кирпичные, плиточные и таблетированные],
                       Экстрагированные [растворимые])
        [*] Происхождение чая (Китайский, Индийский, Цейлонский,
                               Японский, Индокитай, Африканский,
                               Турецкий, Иранский, Прочие)
        [*] Чайная группа (Белый, Зеленый, Желтый, Бирюзовый,
                           Красный, Черный, Прочие)
        **Можно выделить как отдельные классы
    """

    COUNTRIES = ['Китайский', 'Индийский', 'Цейлонский',
                 'Японский', 'Индокитай', 'Африканский',
                 'Турецкий', 'Иранский', 'Прочие']
    GROUP = ['Белый', 'Зеленый', 'Желтый', 'Бирюзовый',
             'Красный', 'Черный', 'Прочие']

    @staticmethod
    def getGroups():
        return Tea.GROUP


    def _find(f, a):
        f = str(f).lower()
        for x in a:
            if str(x).lower() == f:
                return x
        return False

    def __init__(self, name, t, amount, sweet, sour, structure, form, country='Прочие', group='Прочие'):
        # конструктор базового класса
        super().__init__(t, amount, sweet, sour, structure)
        self.name = name

        # Наткнулся на новшество Py 3.10, возможно использую
        # не по назначению, но просто хотел попробвоать
        # Pattern matching:
        # https://www.python.org/dev/peps/pep-0622/
        # https://habr.com/ru/company/yandex_praktikum/blog/547902/
        # https://www.youtube.com/watch?v=0kyy_zKO86U
        # sys.version_info >= (3, 10)
        #
        # match str(form).lower():
        #         case "байховый" | "рассыпной":
        #             self.form = "байховый"
        #         case "прессованный" | "кирпичный" | "плиточный" | "таблетированный":
        #             self.form = "прессованный"
        #         case "экстрагированный" | "растворимый":
        #             self.form = "экстрагированный"
        #         case _:
        #             self.form = "что-то новенькое ;)"
        #
        # Обычный вариант
        tmp = str(form).lower()
        if tmp == "байховый" or tmp == "рассыпной":
            self.form = "Байховый"
        elif tmp == "прессованный" or tmp == "кирпичный" or tmp == "плиточный" or tmp == "таблетированный":
            self.form = "Прессованный"
        elif tmp == "экстрагированный" or tmp == "растворимый":
            self.form = "Экстрагированный"
        else:
            self.form = "Что-то новенькое ;)"

        # Или так
        self.country = Tea._find(country, Tea.COUNTRIES)
        if self.country is False:
            # исключение, такой страны производтва не существует...
            # raise Exception("Такой страны производтва не существует")
            raise CountyNotInRangeError(country)  # Вызываем пользовательский класс исключений

        self.group = Tea._find(group, Tea.GROUP)
        if self.group is False:
            raise Exception("Такой чайной группы не существует")

    # ideal wariant print...
    def __str__(self):
        return f'{self.country} {self.form} {self.get_sweet_or_sour().lower()} {self.group} чай "{self.name}" ({self.amount} л) из группы температура {self.temp}°, состав: "{self.structure}"'

    # Перегрузка оператора сравнения
    def __eq__(self, other): # ==
        return self.name == other.name and self.amount == other.amount


def teaGenerator() -> Tea:
    """Функция - генератор чая"""

    tea_names = ("Иван-чай",)
    try:
        tea_names = get(r"https://raw.githubusercontent.com/linuxforse/"
                         r"random_russian_and_ukraine_name_surname/master/imena_m_ru.txt").text.split()
        if len(tea_names) + len(tea_names) < 2:
            raise Exception("Списки имен пусты")
    except Exception as e:
        print(f"Произошла ошибка при попытке скачать файл с именами, а именно:\n{e}")

    while True:
        names = tea_names
        group = Tea.GROUP[randint(0, len(Tea.GROUP) - 1)]
        country = Tea.COUNTRIES[randint(0, len(Tea.COUNTRIES) - 1)]
        name = names[randint(0, len(names) - 1)]

        t = round(uniform(5,24),1)
        l = round(uniform(0,2),2) 
        # Tea("Иван-чай", 40, 3, True, False, "чайный лист, сахар", "прессованный", "Китайский", "Белый")

        yield Tea(name, t, l, True, False, "чайный лист, сахар", "прессованный", country, group)


def main():
    # Создаем жидкость, например вода
    p = Fluid(32, 2)
    p.name = "Вода"
    print(p)

    # Создаем напиток "Морс"
    d = Drink(36, 1, True, False, "вода, клюква")
    d.name = "Морс"
    d *= 2  # Посредством магии удваиваем его
    print(f"При покупки 2х морсов вы получите {d.amount} л. морса")

    # Создаем чаек
    t = Tea("Иван-чай", 40, 3, True, False, "чайный лист, сахар", "прессованный", "Китайский", "Белый")
    print(t)

    # Разбавляем водичу морсиком
    print(f"Если вылить морс в воду, то получится: {p + d}")

    # Обработка пользовательского исключения
    try:
        # Создаем чаек c несуществующей страной производства
        t = Tea("Особый", 40, 3, True, False, "чайный лист, сахар", "прессованный", "Фиктивный", "Белый")
        print(t)
    except CountyNotInRangeError as e:
        print(f"Ошибка содания чая: {e}")

    teas = []
    teaGen = teaGenerator()
    for i in range(3):
        teas.append(next(teaGen))

    print("\nСгенерированный список: ")
    for t in teas:
        print(t)

    a = teas[0]
    b = teas[1]
    print(f"Проверка перегрузки равенства (false): {a == b}")


if __name__ == '__main__':
    main()
