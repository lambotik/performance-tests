import os
from pathlib import Path

from performance_tests.seeds.schema.result import SeedsResult
from performance_tests.tools.logger import get_logger

# Путь к папке dumps — относительно этого файла (seeds/dumps.py → ../dumps)
DUMPS_DIR = Path(__file__).parent / '..' / 'dumps'

logger = get_logger("SEEDS_DUMPS")

def save_seeds_result(result: SeedsResult, scenario: str):
    """
    Сохраняет результат сидинга (SeedsResult) в JSON-файл.

    :param result: Результат сидинга, сгенерированный билдером.
    :param scenario: Название сценария нагрузки.
    """
    # Создаём папку, если её нет (makedirs не упадёт, если уже существует)
    os.makedirs(DUMPS_DIR, exist_ok=True)

    seeds_file = DUMPS_DIR / f"{scenario}_seeds.json"
    with open(seeds_file, 'w+', encoding='utf-8') as file:
        file.write(result.model_dump_json())
    logger.debug(f"Seeding result saved to file: {seeds_file}")


def load_seeds_result(scenario: str) -> SeedsResult:
    """
    Загружает результат сидинга из JSON-файла.

    :param scenario: Название сценария нагрузки.
    :return: Объект SeedsResult, восстановленный из файла.
    """
    seeds_file = DUMPS_DIR / f"{scenario}_seeds.json"
    # Открываем файл и валидируем его как объект SeedsResult
    with open(seeds_file, 'r', encoding='utf-8') as file:
        logger.debug(f"Seeding result loaded from file: {seeds_file}")
        return SeedsResult.model_validate_json(file.read())