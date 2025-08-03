import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"


class Settings:
    INDEX_PATH = str(DATA_DIR / "my_index2.faiss")
    STRUCTURE_PATH = str(DATA_DIR / "doc_structure.pkl")
    DOCUMENTS_DIR = str(DATA_DIR / "ГОСТ Р ТК 164")


settings = Settings()
