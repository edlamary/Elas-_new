from pathlib import Path

import pandas as pd

from utils import normalize_columns


class BaseSpreadsheetExtractor:
    def extract(self, path: Path) -> pd.DataFrame:
        df = pd.read_excel(path)
        df = normalize_columns(df)
        return df