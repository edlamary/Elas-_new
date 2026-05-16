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
        self._source = source
        self._survey_extractor = survey_extractor
        self._survey_transformer = survey_transformer
        self._schema_maker = schema_maker

    def execute(self):
        query = text("""
                TRUNCATE TABLE fato_atividades,fato_evento_resumo,dim_tempo,dim_evento,dim_participante;
                """)

        engine = Postgres("railway").engine

        with engine.begin() as connection:
            result = connection.execute(query)# type: ignore


        path = self._source.fetch()
        df = self._survey_extractor.extract(path)
        df, df2 = self._survey_transformer.transform(df)
        self._schema_maker.mount(df_survey=df, df_evento=df2)

        return df