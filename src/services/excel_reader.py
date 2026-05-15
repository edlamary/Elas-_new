from pathlib import Path

import pandas as pd

from utils import normalize_columns


class ExcelReader:
    def read_all(self, path: Path) -> dict[str, pd.DataFrame]:
        sheets = pd.read_excel(path, sheet_name=None)

        return {
            name: normalize_columns(df)
            for name, df in sheets.items()
        }