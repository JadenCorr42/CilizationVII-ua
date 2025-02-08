# /// script
# requires-python = ">=3.12"
# dependencies = []
# line-length=120
# ///
import argparse
import os
import shutil
import sys
from collections import defaultdict
from io import StringIO
from pathlib import Path
from xml.etree import ElementTree as ET

if getattr(sys, "frozen", False):
    # If the application is run as a bundle, the PyInstaller bootloader
    # sets the sys._MEIPASS attribute to the path of the bundle's temporary folder.
    base_path = Path(sys._MEIPASS)
else:
    base_path = Path(__file__).parent

resources_path = base_path / "resources"

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
--ai, --ші - Встановити локалізацію створену штучним інтелектом.

Можливі команди для виконання:

- setup_translation, встановити_переклад - Встановлює локалізацію з ресурсів у теку з грою.
- restore_original, відновити_оригінал - Відновлює оригінальні локалізаційні файли з ресурсів у теку з грою.

ТІЛЬКИ ДЛЯ РОЗРОБНИКІВ:
- store_original, зберегти_оригінал  - Копіює всі локалізаційні файли з теки зі грою в теку з ресурсами поряд з цим \
скриптом.
- translation_rate, відсоток_перекладу - Обчислює відсоток перекладених рядків у локалізаційних файлах.
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
        "--ai",
        "--ші",
        action="store_true",
        help="Встановити локалізацію створену штучним інтелектом.",
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
            "translation_rate",
            "відсоток_перекладу",
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
            if args.ai:
                setup_ai_translation(path_to_game)
            else:
                setup_translation(path_to_game)
        case "restore_original" | "відновити_оригінал":
            restore_original(path_to_game)
        case "translation_rate" | "відсоток_перекладу":
            calculate_translation_rate(args.ai)
        case _:
            print("Невідома команда")
            parser.print_help()
            exit(1)


def store_original(path_to_game: Path) -> None:
    for module in CIV_VII_MODULES:
        translation_path = path_to_game.joinpath(
            *CIV_VII_RESOURCES_FOLDER_PATH, module, *CIV_VII_LOC_PATH
        )
        target_path = resources_path / "en_us" / module
        target_path.mkdir(parents=True, exist_ok=True)
        for item in translation_path.iterdir():
            shutil.copy(item, target_path / item.name)


def setup_translation(path_to_game: Path):
    for module in CIV_VII_MODULES:
        localized_path = resources_path / "ua_ua" / module
        target_path = path_to_game.joinpath(
            *CIV_VII_RESOURCES_FOLDER_PATH, module, *CIV_VII_LOC_PATH
        )
        for item in localized_path.iterdir():
            shutil.copy(item, target_path / item.name)


def setup_ai_translation(path_to_game: Path):
    for module in CIV_VII_MODULES:
        localized_path = resources_path / "ua_ai" / module
        target_path = path_to_game.joinpath(
            *CIV_VII_RESOURCES_FOLDER_PATH, module, *CIV_VII_LOC_PATH
        )
        for item in localized_path.iterdir():
            shutil.copy(item, target_path / item.name)


def restore_original(path_to_game: Path):
    for module in CIV_VII_MODULES:
        localized_path = resources_path / "en_us" / module
        target_path = path_to_game.joinpath(
            *CIV_VII_RESOURCES_FOLDER_PATH, module, *CIV_VII_LOC_PATH
        )
        for item in localized_path.iterdir():
            shutil.copy(item, target_path / item.name)


def calculate_translation_rate(ai_translation: bool = False):
    """
    Compare original and translated filed and calculate the amount of translated string.

    By translated means that string is not equal to the original string under the same XML key.

    This rate obviously is not 100 % correct, but it can be used as a rough estimate.
    """
    original_documents = resources_path / "en_us"
    if ai_translation:
        translated_documents = resources_path / "ua_ai"
    else:
        translated_documents = resources_path / "ua_ua"

    total_strings = 0
    translated_strings = 0

    total_per_module_map = defaultdict(int)
    translation_per_module_map = defaultdict(int)
    total_per_file_map = defaultdict(lambda: defaultdict(int))
    translation_per_file_map = defaultdict(lambda: defaultdict(int))

    for module in CIV_VII_MODULES:
        original_path = original_documents / module
        translated_path = translated_documents / module
        for original_file in original_path.iterdir():
            with open(original_file, encoding="utf-8") as base:
                original_tree = ET.parse(base)
                original_root = original_tree.getroot()
            with open(
                translated_path / original_file.name, encoding="utf-8"
            ) as translation:
                translated_tree = ET.parse(translation)
                translated_root = translated_tree.getroot()

            original_texts = original_root.findall(".//Row/Text")
            translated_texts = translated_root.findall(".//Row/Text")

            for original_text, translated_text in zip(original_texts, translated_texts):
                if original_text.text is None:
                    continue
                total_strings += 1
                total_per_module_map[module] += 1
                total_per_file_map[module][original_file.name] += 1
                if (
                    original_text.text.startswith("{")
                    and original_text.text.endswith("}")
                    or original_text.text != translated_text.text
                ):
                    translated_strings += 1
                    translation_per_module_map[module] += 1
                    translation_per_file_map[module][original_file.name] += 1

    print(f"""
Загалом: {total_strings}
Перекладено: {translated_strings}

Відсоток перекладу: {translated_strings / total_strings * 100:.2f}%.

По модулях:
{format_per_module_report(total_per_module_map, translation_per_module_map)}

По файлам:
{format_per_file_report(total_per_file_map, translation_per_file_map)}
""")


def format_per_module_report(
    total_per_module_map: dict[str, int], translation_per_module_map: dict[str, int]
) -> str:
    string_io = StringIO()
    for k, v in total_per_module_map.items():
        translated_v = translation_per_module_map.get(k, 0)
        string_io.write(
            f"{k}: {translation_per_module_map[k]}/{v} ({translated_v / v * 100:.2f}%)\n"
        )
    return string_io.getvalue()


def format_per_file_report(
    total_per_file_map: dict[str, dict[str, int]],
    translation_per_file_map: dict[str, dict[str, int]],
) -> str:
    string_io = StringIO()
    for module, files_map in total_per_file_map.items():
        string_io.write(f"Модуль: {module}\n")
        for file, total in files_map.items():
            translated = translation_per_file_map[module].get(file, 0)
            string_io.write(
                f"\t{file}: {translated}/{total} ({translated / total * 100:.2f}%)\n"
            )
        string_io.write("\n")
    return string_io.getvalue()


if __name__ == "__main__":
    main()
