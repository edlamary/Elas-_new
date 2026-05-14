from pathlib import Path


class LocalSpreadsheetSource:
    def __init__(self, path: Path):
        self._path = path

    def fetch(self) -> Path:
        return self._path