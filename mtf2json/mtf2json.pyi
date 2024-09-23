from pathlib import Path
from typing import Dict, Any


version: str
mm_commit: str


class ConversionError(Exception):
    ...


def read_mtf(path: Path, verbose: bool = False) -> Dict[str, Any]: ...
def write_json(data: Dict[str, Any], path: Path) -> None: ...
