# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
import argparse
import os
import shutil
from pathlib import Path


CIV_VII_FOLDER_NAME = "Sid Meier's Civilization VII"
CIV_VII_RESOURCES_FOLDER_PATH = ["Base", "modules"]
CIV_VII_LOC_PATH = ["text", "en_us"]

CIV_VII_MODULES = [
    "age-antiquity",
    "age-exploration",
    "age-modern",
    "base-standard",
    "core",
]


def fast_find_folder_os(folder_name, search_path="C:\\") -> Path | None:
    for root, dirs, _ in os.walk(search_path):
        if folder_name in dirs:
            return Path(root) / folder_name
    return None


cli_vii_cli_help_text = """
"Civilization VII CLI Tool. 

Спрощує роботу з розробкою та встановленням локалізації"

Аргументи:

--path, --шлях - Шлях до теки з грою Civilization VII. Якщо не задано, скрипт спробує знайти теку (це може зайняти час).

Можливі команди для виконання:

ТІЛЬКИ ДЛЯ РОЗРОБНИКІВ:
- store_original, зберегти_оригінал  - Копіює всі локалізаційні файли з теки зі грою в теку з ресурсами поряд з цим \
скриптом.
- setup_translation, встановити_переклад - Встановлює локалізацію з ресурсів у теку з грою.
- restore_original, відновити_оригінал - Відновлює оригінальні локалізаційні файли з ресурсів у теку з грою.
"""


def main() -> None:
    parser = argparse.ArgumentParser(
        description=cli_vii_cli_help_text,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--path",
        "--шлях",
        type=str,
        default=None,
        required=False,
        help="Шлях до теки з грою Civilization VII.",
    )
    parser.add_argument(
        "command",
        choices=[
            "store_original",
            "зберегти_оригінал",
            "setup_translation",
            "встановити_переклад",
            "restore_original",
            "відновити_оригінал",
        ],
        help="Дія яка має бути виконана скриптом",
    )
    args = parser.parse_args()

    if args.path:
        path_to_game = Path(args.path)
    else:
        path_to_game = fast_find_folder_os(CIV_VII_FOLDER_NAME)

    match args.command:
        case "store_original" | "зберегти_оригінал":
            store_original(path_to_game)
        case "setup_translation" | "встановити_переклад":
            setup_translation(path_to_game)
        case "restore_original" | "відновити_оригінал":
            restore_original(path_to_game)
        case _:
            print("Невідома команда")
            parser.print_help()
            exit(1)


def store_original(path_to_game: Path) -> None:
    for module in CIV_VII_MODULES:
        translation_path = path_to_game.joinpath(
            *CIV_VII_RESOURCES_FOLDER_PATH, module, *CIV_VII_LOC_PATH
        )
        target_path = Path(__file__).parent / "resources" / "en_us" / module
        target_path.mkdir(parents=True, exist_ok=True)
        for item in translation_path.iterdir():
            shutil.copy(item, target_path / item.name)


def setup_translation(path_to_game: Path):
    for module in CIV_VII_MODULES:
        localized_path = Path(__file__).parent / "resources" / "ua_ua" / module
        target_path = path_to_game.joinpath(
            *CIV_VII_RESOURCES_FOLDER_PATH, module, *CIV_VII_LOC_PATH
        )
        for item in localized_path.iterdir():
            shutil.copy(item, target_path / item.name)


def restore_original(path_to_game: Path):
    for module in CIV_VII_MODULES:
        localized_path = Path(__file__).parent / "resources" / "en_us" / module
        target_path = path_to_game.joinpath(
            *CIV_VII_RESOURCES_FOLDER_PATH, module, *CIV_VII_LOC_PATH
        )
        for item in localized_path.iterdir():
            shutil.copy(item, target_path / item.name)


if __name__ == "__main__":
    main()
