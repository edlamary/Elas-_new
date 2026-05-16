from pathlib import Path

import pandas as pd
from db.postgres import Postgres
from utils import save_debug_dataframe


class SchemaMaker:
    def __init__(self):
        self.db_engine = Postgres("railway").engine
    
    def _generate_sk(self, df:pd.DataFrame, column_name:str):
        df = df.reset_index(drop=True)
        df[column_name] = df.index + 1
        return df
    
    def _mount_dim_participant(self, df_survey:pd.DataFrame):
        df_survey = self._generate_sk(df_survey, "sk_participante")
        df_dim_participante = df_survey[[
            "sk_participante",
            "idade",
            "ano_ensino_medio"
        ]]
        return df_survey, df_dim_participante
    
    def _mount_dim_time(self, df_survey:pd.DataFrame):
        datas = pd.date_range(
            start=df_survey["datahora"].min().date(),
            end=df_survey["datahora"].max().date(),
            freq="D"
        )

        dim_tempo = pd.DataFrame({"data": datas})

        dim_tempo["sk_tempo"] = dim_tempo["data"].dt.strftime("%Y%m%d").astype(int)
        dim_tempo["dia"] = dim_tempo["data"].dt.day
        dim_tempo["mes"] = dim_tempo["data"].dt.month
        dim_tempo["ano"] = dim_tempo["data"].dt.year

        # normalizar tipo da data
        df_survey["data"] = pd.to_datetime(df_survey["datahora"]).dt.date
        dim_tempo["data"] = pd.to_datetime(dim_tempo["data"]).dt.date
        
        return df_survey, dim_tempo
    
    def _generate_date_column(self, df:pd.DataFrame, column_to_extract:str):
        df["data"] = pd.to_datetime(df[column_to_extract]).dt.date
        
        return df
    

    def mount(self, df_survey: pd.DataFrame, df_fact_event_summary: pd.DataFrame):
        df_survey, df_dim_participante = self._mount_dim_participant(df_survey=df_survey)

        df_fact_event_summary = self._generate_sk(df_fact_event_summary, "sk_evento")
        df_fact_event_summary["tema"] = "Pixels e Algoritmos"
        df_fact_event_summary["tipo_de_acao"] = "oficina"

        df_survey = self._generate_date_column(df=df_survey, column_to_extract="datahora")
        df_fact_event_summary = self._generate_date_column(df=df_fact_event_summary, column_to_extract="data")

        # FK_EVENTO
        df_survey = df_survey.merge(
            df_fact_event_summary[["data", "sk_evento"]],
            on="data",
            how="left"
        )

        df_survey, dim_time = self._mount_dim_time(df_survey=df_survey)
        
        # FK_TEMPO
        df_survey = df_survey.merge(
            dim_time[["data", "sk_tempo"]],
            on="data",
            how="left"
        )


        df_fact = df_survey.copy()
        df_fact = df_fact.rename(columns={
            "crescimento_interesse_percentual": "crescimento_de_interesse",
        })
        df_fact = self._generate_sk(df_fact, "sk_fato_atividade")
        df_fact_event_summary["sk_tempo"] = pd.to_datetime(df_fact_event_summary["data"]).dt.strftime("%Y%m%d").astype(int)
        
        dim_event = df_fact_event_summary.copy()
        dim_event.drop(columns=["qtd_participantes","data","sk_tempo"], inplace=True)
        
        df_fact_event_summary = df_fact_event_summary.drop(columns=["data", "tema","tipo_de_acao"], errors="ignore")
        df_fact_event_summary = df_fact_event_summary.reset_index(drop=True)
        df_fact_event_summary["sk_fato_evento_resumo"] = df_fact_event_summary.index + 1

        df_fact.drop(columns=[
            'datahora', 'idade', 'ano_ensino_medio', 'relevancia_temas',
        'aplicabilidade_conhecimento', 'nps_oficina','interesse_stem_depois', 'data','coeficiente_de_qualidade_categorizado'
        ], inplace=True)
        dim_time.drop(columns=["data"], inplace=True)
        
        self._save_debug_files(fact_activities=df_fact, dim_event=dim_event, dim_time=dim_time,
        dim_participant=df_dim_participante, fact_event_summary=df_fact_event_summary)
        
        self._persist(
            fact_activities=df_fact, dim_event=dim_event, dim_time=dim_time,
        dim_participant=df_dim_participante, fact_event_summary=df_fact_event_summary
        )
    
    def _save_debug_files(
        self,
        fact_activities: pd.DataFrame,
        fact_event_summary: pd.DataFrame,
        dim_time: pd.DataFrame,
        dim_event: pd.DataFrame,
        dim_participant: pd.DataFrame
    ):
        debug_files = {
            "clean_fato_atividades.xlsx": fact_activities,
            "clean_fato_evento_resumo.xlsx": fact_event_summary,
            "clean_dim_tempo.xlsx": dim_time,
            "clean_dim_evento.xlsx": dim_event,
            "clean_dim_participante.xlsx": dim_participant,
        }

        for filename, df in debug_files.items():
            save_debug_dataframe(
                df=df,
                output_path=Path(f"src/debug/{filename}")
            )
            
    def _persist(
        self,
        dim_time: pd.DataFrame,
        dim_event: pd.DataFrame,
        dim_participant: pd.DataFrame,
        fact_activities: pd.DataFrame,
        fact_event_summary: pd.DataFrame
    ):
        dim_time.to_sql(
            "dim_tempo",
            con=self.db_engine,
            index=False,
            if_exists="append"
        )

        dim_event.to_sql(
            "dim_evento",
            con=self.db_engine,
            index=False,
            if_exists="append"
        )

        dim_participant.to_sql(
            "dim_participante",
            con=self.db_engine,
            index=False,
            if_exists="append"
        )

        fact_activities.to_sql(
            "fato_atividades",
            con=self.db_engine,
            index=False,
            if_exists="append"
        )

        fact_event_summary.to_sql(
            "fato_evento_resumo",
            con=self.db_engine,
            index=False,
            if_exists="append"
        )