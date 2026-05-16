from sqlalchemy import text

from db.postgres import Postgres
from interfaces.spreadsheet_source import SpreadsheetSource
from services.schema_maker import SchemaMaker
from services.survey_extractor import SurveyExtractor
from services.survey_transformer import SurveyTransformer


class SurveyProcessingPipeline:

    def __init__(
        self,
        source: SpreadsheetSource,
        survey_extractor: SurveyExtractor,
        survey_transformer: SurveyTransformer,
        schema_maker: SchemaMaker,
    ):
        self._source: SpreadsheetSource = source
        self._survey_extractor: SurveyExtractor = survey_extractor
        self._survey_transformer: SurveyTransformer = survey_transformer
        self._schema_maker: SchemaMaker = schema_maker

    def execute(self):
        self._clean_database()
        path = self._source.fetch()
        survey_df = self._survey_extractor.extract(path)
        survey_df, grouped_programs_df = self._survey_transformer.transform(survey_df)
        self._schema_maker.mount(df_survey=survey_df, df_fact_event_summary=grouped_programs_df)
    
    
    def _clean_database(self):
        query = text("""
                TRUNCATE TABLE fato_atividades,fato_evento_resumo,dim_tempo,dim_evento,dim_participante;
                """)
        engine = Postgres("railway").engine

        with engine.begin() as connection:
            result = connection.execute(query) # type: ignore