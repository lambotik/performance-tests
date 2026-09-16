import time

from faker import Faker
from faker.providers.python import TEnum


class Fake:
    """
    Класс для генерации случайных тестовых данных с использованием библиотеки Faker.
    """

    def __init__(self, faker: Faker):
        """
        :param faker: Экземпляр класса Faker, который будет использоваться для генерации данных.
        """
        self.faker = faker

    def enum(self, value: type[TEnum]) -> TEnum:
        """
        Выбирает случайное значение из enum-типа.

        :param value: Enum-класс для генерации значения.
        :return: Случайное значение из перечисления.
        """
        return self.faker.enum(value)

    def email(self) -> str:
        """
        Генерирует случайный email.

        Если не указан, будет использован случайный домен.
        :return: Случайный email.
        """
        return f"{time.time()}.{self.faker.email()}"

    def category(self) -> str:
        """
        Генерирует случайную категорию покупки из предопределённого списка.

        Используется для имитации типов расходов в системах, моделирующих
        пользовательские транзакции или поведение при оплате товаров и услуг.

        :return: Случайная категория (например, 'gas', 'taxi', 'supermarkets' и т.д.).
        """
        return self.faker.random_element([
            "gas",
            "taxi",
            "tolls",
            "water",
            "beauty",
            "mobile",
            "travel",
            "parking",
            "catalog",
            "internet",
            "satellite",
            "education",
            "government",
            "healthcare",
            "restaurants",
            "electricity",
            "supermarkets",
        ])

    def last_name(self) -> str:
        """
        Генерирует случайную фамилию.

        :return: Случайная фамилия.
        """
        return self.faker.last_name()

    def first_name(self) -> str:
        """
        Генерирует случайное имя.

        :return: Случайное имя.
        """
        return self.faker.first_name()

    def middle_name(self) -> str:
        """
        Генерирует случайное отчество/среднее имя.

        :return: Случайное отчество.
        """
        return self.faker.first_name()

    def phone_number(self) -> str:
        """
        Генерирует случайный номер телефона.

        :return: Случайный номер телефона.
        """
        return self.faker.phone_number()

    def float(self, start: int = 1, end: int = 100) -> float:
        """
        Генерирует случайное число с плавающей запятой в указанном диапазоне.

        :param start: Начало диапазона (включительно).
        :param end: Конец диапазона (включительно).
        :return: Случайное число с плавающей запятой.
        """
        return self.faker.pyfloat(min_value=start, max_value=end, right_digits=2)

    def amount(self) -> float:
        """
        Генерирует случайную денежную сумму.

        :return: Сумма от 1 до 1000.
        """
        return self.float(1, 1000)

    def proto_enum(self, value):
        """
        Выбирает случайное значение из Protobuf Enum.

        :param value: Класс Protobuf Enum (например, OperationStatus).
        :return: Случайное числовое значение (или элемент) из перечисления.
        """
        # 1. Если это стандартный сгенерированный Protobuf enum (имеет DESCRIPTOR)
        if hasattr(value, 'DESCRIPTOR'):
            # Извлекаем числовые значения (number) из дескриптора
            values = [v.number for v in value.DESCRIPTOR.values]
            return self.faker.random_element(values)

        # 2. Если это стандартный Python Enum (например, из библиотеки proto-plus или betterproto)
        if hasattr(value, '__members__'):
            return self.faker.random_element(list(value))

        # 3. Фоллбэк: если это просто класс с целочисленными атрибутами
        values = [v for k, v in vars(value).items() if not k.startswith('_') and isinstance(v, int)]
        if values:
            return self.faker.random_element(values)

        raise ValueError(f"Не удалось извлечь значения из {value}")


# Создаем экземпляр класса Fake с использованием Faker
fake = Fake(faker=Faker())
