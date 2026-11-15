
import json
from datetime import date

from io import TextIOWrapper
from pathlib import Path
from typing import Dict, List

_DATA_DIR: str = "tmp/data"
_SRC_FILE: str = "xiaomi_weights.json"


def get_weights(user: str = "MicoDa", sort_by_date: bool = True) -> Dict[str, float]:
    file_path: Path = Path(
        Path(__file__).parents[3] / f"{_DATA_DIR}/{_SRC_FILE}"
    )
    src: TextIOWrapper = open(file=file_path)
    data: Dict[str, float] = {
        _extract_date(k["date"]): k["weight"] for k in json.load(src)["records"]
        if k["user"] == user
    }
    src.close()

    if sort_by_date:
        return _sort_data(src_data=data)
    return data


def daily_moving_average(sorted_data: Dict[str, float], decimals: int = 2) -> Dict[str, float]:
    """
    7-Day Moving Average
    """
    data: Dict[str, float] = {}
    for i in range(6, len(sorted_data)):
        window: List[tuple] = list(sorted_data.items())[i - 6: i + 1]
        window_average: float = sum(value for _, value in window) / 7
        data[window[6][0]] = round(window_average, decimals)
    return data


def _extract_date(utc_date: str) -> str:
    return str(utc_date.split("T")[0])


def _sort_data(src_data: Dict[str, float]) -> Dict[str, float]:
    sorted_data: List[tuple] = sorted(
        src_data.items(),
        key=lambda item: date.fromisoformat(item[0])
    )
    return dict(sorted_data)


__all__ = ["get_weights", "weekly_moving_average"]

if __name__ == "__main__":
    src_data: Dict[str, float] = get_weights(sort_by_date=True)
    daily_moving_average(sorted_data=src_data)
