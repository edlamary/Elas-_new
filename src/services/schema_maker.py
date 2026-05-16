from pathlib import Path

import pandas as pd
from db.postgres import Postgres
from utils import save_debug_dataframe


class SchemaMaker:
    def __init__(self):
        pass

    def mount(self, df_survey: pd.DataFrame, df_evento: pd.DataFrame):

        # -----------------------
        # PARTICIPANTE (DIM)
        # -----------------------
        df_survey = df_survey.reset_index(drop=True)
        df_survey["sk_participante"] = df_survey.index + 1

        df_dim_participante = df_survey[[
            "sk_participante",
            "idade",
            "ano_ensino_medio"
        ]]

        # -----------------------
        # EVENTO (DIM)
        # -----------------------
        df_evento = df_evento.reset_index(drop=True)
        df_evento["sk_evento"] = df_evento.index + 1

        df_evento["tema"] = "Pixels e Algoritmos"
        df_evento["tipo_de_acao"] = "oficina"

        # -----------------------
        # NORMALIZA DATA (BASE DE JOIN)
        # -----------------------
        df_survey["data"] = pd.to_datetime(df_survey["datahora"]).dt.date
        df_evento["data"] = pd.to_datetime(df_evento["data"]).dt.date

        # -----------------------
        # FK EVENTO
        # -----------------------
        df_survey = df_survey.merge(
            df_evento[["data", "sk_evento"]],
            on="data",
            how="left"
        )

        # -----------------------
        # DIM TEMPO
        # -----------------------
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

        # -----------------------
        # FK TEMPO
        # -----------------------
        df_survey = df_survey.merge(
            dim_tempo[["data", "sk_tempo"]],
            on="data",
            how="left"
        )

        # -----------------------
        # FATO FINAL
        # -----------------------
        df_fact = df_survey.copy()

        df_fact = df_fact.rename(columns={
            "sk_participante": "sk_participante",
            "sk_evento": "sk_evento",
            "sk_tempo": "sk_tempo",
            "crescimento_interesse_percentual": "crescimento_de_interesse",
        })
        df_fact = df_fact.reset_index(drop=True)
        df_fact["sk_fato_atividade"] = df_fact.index + 1
        dim_tempo.drop(columns=["data"], inplace=True)

        df_evento["sk_tempo"] = pd.to_datetime(df_evento["data"]).dt.strftime("%Y%m%d").astype(int)
        dim_evento = df_evento.copy()
        df_evento = df_evento.drop(columns=["data", "tema","tipo_de_acao"], errors="ignore")
        df_evento = df_evento.reset_index(drop=True)
        df_evento["sk_fato_evento_resumo"] = df_evento.index + 1
        dim_evento.drop(columns=["qtd_participantes","data","sk_tempo"], inplace=True)

        df_fact.drop(columns=[
            'datahora', 'idade', 'ano_ensino_medio', 'relevancia_temas',
        'aplicabilidade_conhecimento', 'nps_oficina','interesse_stem_depois',        'data'
        ], inplace=True)
        print(df_fact.columns)

        print(df_fact.head(10), df_dim_participante.head(10), df_evento.head(10), dim_tempo.head(10), dim_evento.head(10))
        debug_path = Path("src/debug/clean_fato_atividades.xlsx")
        save_debug_dataframe(df=df_fact, output_path=debug_path)
        debug_path = Path("src/debug/clean_fato_evento_resumo.xlsx")
        save_debug_dataframe(df=df_evento, output_path=debug_path)
        debug_path = Path("src/debug/clean_dim_tempo.xlsx")
        save_debug_dataframe(df=dim_tempo, output_path=debug_path)
        debug_path = Path("src/debug/clean_dim_evento.xlsx")
        save_debug_dataframe(df=dim_evento, output_path=debug_path)
        debug_path = Path("src/debug/clean_dim_participante.xlsx")
        save_debug_dataframe(df=df_dim_participante, output_path=debug_path)
        dim_tempo.to_sql("dim_tempo",con=Postgres("railway").engine,  index=False, if_exists="append")
        dim_evento.to_sql("dim_evento",con=Postgres("railway").engine,  index=False, if_exists="append")
        df_fact.drop(columns=["coeficiente_de_qualidade_categorizado"], inplace=True)
        df_dim_participante.to_sql("dim_participante",con=Postgres("railway").engine,  index=False, if_exists="append")
        df_fact.to_sql("fato_atividades",con=Postgres("railway").engine,  index=False, if_exists="append")
        df_evento.to_sql("fato_evento_resumo",con=Postgres("railway").engine,  index=False, if_exists="append")
        return df_fact, df_dim_participante, df_evento, dim_tempo