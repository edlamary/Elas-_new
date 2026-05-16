from pathlib import Path

import pandas as pd

from utils import save_debug_dataframe


class SurveyTransformer:
    def __init__(self):
        pass

    def transform(self, df:pd.DataFrame):
        print(df.head(5),"AOBA")
        df = self.rename_columns(df)
        df = df.dropna(subset=["datahora"])

        mapa_interesse = {
            "Nada interessada": 1,
            "Pouco interessada": 2,
            "Neutra": 3,
            "Interessada": 4,
            "Muito interessada": 5
        }


        df["interesse_stem_antes"] = (
            df["interesse_stem_antes_category"]
            .map(mapa_interesse)
            .astype(int)
        )


        df["crescimento_interesse_percentual"] = (
            (df["interesse_stem_depois"] - df["interesse_stem_antes"]) * 20
        )


        df["cresceu_interesse"] = (
            df["crescimento_interesse_percentual"] > 0
        )

        df["coeficiente_de_qualidade"] = (
            (df["aplicabilidade_conhecimento"] + df["relevancia_temas"]) / 2
        )

        labels = [
            "Muito baixo",
            "Baixo",
            "Médio",
            "Alto",
            "Muito alto"
        ]

        df["coeficiente_de_qualidade_categorizado"] = pd.cut(
            df["coeficiente_de_qualidade"],
            bins=[0, 1, 2, 3, 4, 5],
            include_lowest=True,
            labels=labels
        )

        df["tem_interesse_em_stem"] = (
            df["interesse_stem_depois"] > 3
        )

        map_bool = {
            "Sim": True,
            "Não": False
        }

        df["participacao_previa_stem"] = (
            df["participacao_previa_stem_category"]
            .map(map_bool)
            .astype(bool)
        )


        print(df.head(5))
        


        df["data"] = df["datahora"].dt.date
        df["ano_ensino_medio"] = (
            df["ano_ensino_medio"]
            .astype(str)
            .str.extract(r"(\d+)", expand=False)
            .astype("Int64")
        )
        df_por_data = df.groupby("data").size().reset_index(name="qtd_participantes")
        self.clean_survey_df(df=df)
        debug_path = Path("src/debug/semi_clean_df_survey.xlsx")
        save_debug_dataframe(df=df, output_path=debug_path)

        
        return  df,df_por_data
    
    def clean_survey_df(self,df: pd.DataFrame):
        df.drop(columns=["space", "carreira_futura","interesse_stem_antes_category",
        "interesse_stem_antes","participacao_previa_stem_category","clareza_explicacoes","compreensao_pixel_algoritmos","nivel_atividades","interesse_carreira_stem"],inplace=True)
    
    def rename_columns(self,df:pd.DataFrame):
        df.columns = [
        "datahora",
        "idade",
        "ano_ensino_medio",
        "interesse_stem_antes_category",
        "participacao_previa_stem_category",
        "carreira_futura",
        "relevancia_temas",
        "clareza_explicacoes",
        "compreensao_pixel_algoritmos",
        "nivel_atividades",
        "interesse_stem_depois",
        "interesse_carreira_stem",
        "aplicabilidade_conhecimento",
        "space",
        "space",
        "space",
        "space",
        "nps_oficina"
        ]
        return df