from services.excel_reader import ExcelReader
from services.sharepoint_spreadsheet_source import SharePointSpreadsheetSource
from services.schema_maker import SchemaMaker
from services.survey_extractor import SurveyExtractor
from services.survey_processing_pipeline import SurveyProcessingPipeline
from services.survey_transformer import SurveyTransformer


def main():
    SurveyProcessingPipeline(
        source=SharePointSpreadsheetSource(),
        schema_maker=SchemaMaker(),
        survey_transformer=SurveyTransformer(),
        survey_extractor=SurveyExtractor(ExcelReader()),
    ).execute()


if __name__ == "__main__":
    main()