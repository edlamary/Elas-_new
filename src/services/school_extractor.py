from pathlib import Path
from services.excel_reader import ExcelReader

class SchoolExtractor:
  def __init__(self, reader: ExcelReader):
      self._reader = reader

  
  def extract(self, path:Path):
    sheets = self._reader.read_all(path)
    print(sheets)