
import json

from io import TextIOWrapper
from pathlib import Path
from typing import Dict

_DATA_DIR: str = "tmp/data"


def get_weights() -> Dict[str, float]:
    src_file: str = "xiaomi_weights.json"
    file_path: Path = Path(
        Path(__file__).parents[3] / f"{_DATA_DIR}/{src_file}"
    )
    print(file_path)
    src: TextIOWrapper = open(file=file_path)
    data: Dict[float] = {
        extract_date(k["date"]): k["weight"] for k in json.load(src)["records"]
    }
    src.close()
    return data


def extract_date(utc_date: str) -> str:
    return str(utc_date.split("T")[0])


__all__ = ["get_weights"]

if __name__ == "__main__":
    get_weights()
