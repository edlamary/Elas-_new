from interfaces.spreadsheet_source import SpreadsheetSource
from services.spreadsheet_extractor import SpreadsheetExtractor


class SpreadsheetPipeline:

    def __init__(
        self,
        source: SpreadsheetSource,
        extractor: SpreadsheetExtractor
    ):
        self._source = source
        self._extractor = extractor

    def execute(self):
        path = self._source.fetch()
        df = self._extractor.extract(path)

        return df