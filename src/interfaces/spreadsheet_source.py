from pathlib import Path
from typing import Protocol

class SpreadsheetSource(Protocol):
    def fetch(self) -> Path:
        ...