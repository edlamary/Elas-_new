

from pathlib import Path

from services.excel_reader import ExcelReader
from services.local_spreadsheet_source import LocalSpreadsheetSource
from services.schema_maker import SchemaMaker
# from services.school_extractor import SchoolExtractor
from services.survey_extractor import SurveyExtractor
from services.survey_processing_pipeline import SurveyProcessingPipeline
from services.survey_transformer import SurveyTransformer


BASE_DIR = Path(__file__).resolve().parent

def main():
    survey_path = BASE_DIR / "data" / "Formulário de feeback oficina (respostas).xlsx"
    # school_path = BASE_DIR / "data" / "Parceiros (escolas, entidades, etc).xlsx"
    
    # SchoolExtractor(ExcelReader()).extract(school_path)
    SurveyProcessingPipeline(source=LocalSpreadsheetSource(path=survey_path), schema_maker=SchemaMaker(), survey_transformer=SurveyTransformer(), survey_extractor=SurveyExtractor(ExcelReader())).execute()

if __name__ == "__main__":
  main()