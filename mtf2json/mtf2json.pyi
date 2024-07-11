from pathlib import Path
from typing import Dict, Any


version: str
mm_version: str


class ConversionError(Exception):
    ...


def read_mtf(path: Path) -> Dict[str, Any]: ...
def write_json(data: Dict[str, Any], path: Path) -> None: ...
