import json
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable, List

from extractors.utils import get_logger

logger = get_logger(__name__)

def _ensure_directory(path: Path) -> None:
    if not path.parent.exists():
        logger.info("Creating directory %s", path.parent)
        path.parent.mkdir(parents=True, exist_ok=True)

def export_to_json(records: Iterable[Any], path: Path) -> None:
    """
    Export records (list or iterable of dict-like objects) into a JSON file.
    Adds metadata with export timestamp and record count.
    """
    records_list: List[Any] = list(records)
    payload = {
        "meta": {
            "exported_at": datetime.utcnow().isoformat() + "Z",
            "record_count": len(records_list),
        },
        "data": records_list,
    }

    _ensure_directory(path)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    logger.info(
        "Exported %s records to %s",
        len(records_list),
        path,
    )