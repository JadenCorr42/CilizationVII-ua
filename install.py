# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
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

def main() -> None:
    target_folder = fast_find_folder_os(CIV_VII_FOLDER_NAME)
    for module in CIV_VII_MODULES:
        translation_path = target_folder.joinpath(*CIV_VII_RESOURCES_FOLDER_PATH, module, *CIV_VII_LOC_PATH)
        target_path = Path(__file__).parent / "resources" / "en_us" / module
        target_path.mkdir(parents=True, exist_ok=True)
        for item in translation_path.iterdir():
            shutil.copy(item, target_path / item.name)

if __name__ == "__main__":
    main()
