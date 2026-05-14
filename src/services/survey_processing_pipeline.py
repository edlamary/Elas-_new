from interfaces.spreadsheet_source import SpreadsheetSource
from services.base_spreadsheet_extractor import BaseSpreadsheetExtractor


class SurveyProcessingPipeline:

    def __init__(
        self,
        source: SpreadsheetSource,
        extractor: BaseSpreadsheetExtractor
    ):
        self._source = source
        self._extractor = extractor

    def execute(self):
        path = self._source.fetch()
        df = self._extractor.extract(path)

        return df