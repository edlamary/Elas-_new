from pathlib import Path
import pandas as pd


def save_debug_dataframe(df: pd.DataFrame, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df.to_excel(output_path, index=False)