import re
import unicodedata
import pandas as pd


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    normalized_columns: list[str] = []

    for col in df.columns:
        normalized = (
            unicodedata.normalize("NFKD", str(col))
            .encode("ascii", "ignore")
            .decode("utf-8")
            .strip()
            .lower()
        )

        normalized = re.sub(r"[^\w\s]", "", normalized)
        normalized = normalized.replace(" ", "_")
        normalized = re.sub(r"_+", "_", normalized)
        normalized_columns.append(normalized)

    df.columns = normalized_columns

    return df