
import json
from datetime import date

from io import TextIOWrapper
from pathlib import Path
from typing import Dict, List

_DATA_DIR: str = "tmp/data"


def get_weights(user: str = "MicoDa", sort_by_date: bool = True) -> Dict[str, float]:
    src_file: str = "xiaomi_weights.json"
    file_path: Path = Path(
        Path(__file__).parents[3] / f"{_DATA_DIR}/{src_file}"
    )
    print(file_path)
    src: TextIOWrapper = open(file=file_path)
    data: Dict[str, float] = {
        extract_date(k["date"]): k["weight"] for k in json.load(src)["records"]
        if k["user"] == user
    }
    src.close()

    if sort_by_date:
        sorted_data: List[tuple] = sorted(
            data.items(),
            key=lambda item: date.fromisoformat(item[0])
        )
        data: Dict[str, float] = dict(sorted_data)

    return data


def extract_date(utc_date: str) -> str:
    return str(utc_date.split("T")[0])


__all__ = ["get_weights"]

if __name__ == "__main__":
    get_weights()
