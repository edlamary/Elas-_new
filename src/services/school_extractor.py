from pathlib import Path
import re

import pandas as pd
from services.excel_reader import ExcelReader
from utils import save_debug_dataframe

class SchoolExtractor:
  def __init__(self, reader: ExcelReader):
      self._reader = reader

  
  def extract(self, path:Path):
    sheets = self._reader.read_all(path)
    final_df = pd.DataFrame()
    for _, sheet in sheets.items():
      final_df = pd.concat([final_df, sheet], ignore_index=True) # type: ignore

    final_df.columns = [
       "name","space","space","space","space","space","had_event","space","address"
    ]

    final_df.drop(columns=["space"], inplace=True)
    final_df["data_oficina"] = final_df["had_event"].apply(extrair_data)


    final_df = final_df[final_df["name"] != "Escola/Instituição"]
    debug_path = Path("src/debug/clean_schools.xlsx")
    save_debug_dataframe(df=final_df, output_path=debug_path)
    print(final_df.head(50))
    return final_df

def extrair_data(texto:str):
    if pd.isna(texto):
        return None

    texto = texto.lower()

    # caso "abril/maio 2025"
    match = re.search(r"(jan|fev|mar|abr|mai|jun|jul|ago|set|out|nov|dez|janeiro|fevereiro|março|abril|maio|junho|julho|agosto|setembro|outubro|novembro|dezembro)[^\d]*(\d{4})", texto)
    if match:
        mes = match.group(1)
        ano = int(match.group(2))

        meses = {
            "jan": 1, "janeiro": 1,
            "fev": 2, "fevereiro": 2,
            "mar": 3, "março": 3,
            "abr": 4, "abril": 4,
            "mai": 5, "maio": 5,
            "jun": 6, "junho": 6,
            "jul": 7, "julho": 7,
            "ago": 8, "agosto": 8,
            "set": 9, "setembro": 9,
            "out": 10, "outubro": 10,
            "nov": 11, "novembro": 11,
            "dez": 12, "dezembro": 12,
        }

        mes_num = meses.get(mes[:3], 1)
        return pd.Timestamp(year=ano, month=mes_num, day=1)

    # caso só ano tipo "(em 2023)"
    match = re.search(r"(\d{4})", texto)
    if match:
        return pd.Timestamp(year=int(match.group(1)), month=1, day=1)

    return None