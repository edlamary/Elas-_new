

from pathlib import Path

from services.local_spreadsheet_source import LocalSpreadsheetSource
from services.survey_extractor import SurveyExtractor
from services.survey_processing_pipeline import SurveyProcessingPipeline


BASE_DIR = Path(__file__).resolve().parent

def main():
  pass

if __name__ == "__main__":
    survey_path = BASE_DIR / "data" / "Formulário de feeback oficina (respostas).xlsx"
    SurveyProcessingPipeline(source=LocalSpreadsheetSource(path=survey_path), extractor=SurveyExtractor()).execute()
