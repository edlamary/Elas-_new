

from services.local_spreadsheet_source import LocalSpreadsheetSource
from services.spreadsheet_extractor import SpreadsheetExtractor
from services.spreadsheet_pipeline import SpreadsheetPipeline


def main():
  pass

if __name__ == "__main__":
    SpreadsheetPipeline(source=LocalSpreadsheetSource(), extractor=SpreadsheetExtractor()).execute()
