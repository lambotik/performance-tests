import os

from performance_tests.seeds.schema.result import SeedsResult

# Путь к папке dumps — относительно этого файла (seeds/dumps.py → ../dumps)
DUMPS_DIR = os.path.join(os.path.dirname(__file__), '..', 'dumps')


def save_seeds_result(result: SeedsResult, scenario: str):
    """
    Сохраняет результат сидинга (SeedsResult) в JSON-файл.

    :param result: Результат сидинга, сгенерированный билдером.
    :param scenario: Название сценария нагрузки.
    """
    # Создаём папку, если её нет (makedirs не упадёт, если уже существует)
    os.makedirs(DUMPS_DIR, exist_ok=True)

    filepath = os.path.join(DUMPS_DIR, f'{scenario}_seeds.json')
    with open(filepath, 'w+', encoding='utf-8') as file:
        file.write(result.model_dump_json())


def load_seeds_result(scenario: str) -> SeedsResult:
    """
    Загружает результат сидинга из JSON-файла.

    :param scenario: Название сценария нагрузки.
    :return: Объект SeedsResult, восстановленный из файла.
    """
    filepath = os.path.join(DUMPS_DIR, f'{scenario}_seeds.json')
    # Открываем файл и валидируем его как объект SeedsResult
    with open(filepath, 'r', encoding='utf-8') as file:
        return SeedsResult.model_validate_json(file.read())