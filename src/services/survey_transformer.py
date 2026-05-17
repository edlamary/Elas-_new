from pathlib import Path

import pandas as pd

from utils import save_debug_dataframe


class SurveyTransformer:
    def __init__(self):
        pass

    def transform(self, df:pd.DataFrame):
        survey_df: pd.DataFrame = self._clean_survey_df(df=df)
        
        # Porcentagem de crescimento de interesse individual
        survey_df = self._get_individual_interest_growth_percentage(df=survey_df)
        
        # Porcentagem de alunos que apresentaram crescimento no interesse
        survey_df = self._get_students_with_interest_growth(df=survey_df)
        
        # Avaliar a efetividade das oficinas com base na satisfação e aplicabilidade
        survey_df = self._generate_quality_coefficient(df=survey_df)
        
        # Analisar fatores que influenciam a recomendação do projeto
        # Requisito não necessitou de contas ou transformações pesadas, colunas buscadas necessárias adquiridas na extração.
        
        # Analisar distribuição de participantes entre os anos do EM no programa
        survey_df = self._transform_high_school_year(df=survey_df)

        # Calcular % de pessoas com intenção de seguir na àrea de STEM
        survey_df = self._find_students_interested_in_stem_careers(df=survey_df)
        
        # Evolução do número de participantes das oficinas ao longo do tempo
        survey_df, grouped_programs_df = self._group_by_programs(survey_df)
        
        # Comparar satisfação entre participantes com experiência prévia e iniciantes
        survey_df = self._get_experienced_and_beginner_participants(df=survey_df)

        self._drop_unused_columns(df=survey_df)
        debug_path = Path("src/debug/semi_clean_df_survey.xlsx")
        save_debug_dataframe(df=df, output_path=debug_path)
        
        return  survey_df,grouped_programs_df
    
    
    def _clean_survey_df(self, df:pd.DataFrame)-> pd.DataFrame:
        df = self.rename_columns(df)
        df = df.dropna(subset=["datahora"])
        return df
    
    def _get_individual_interest_growth_percentage(self, df:pd.DataFrame):
        interest_map = {
            "Nada interessada": 1,
            "Pouco interessada": 2,
            "Neutra": 3,
            "Interessada": 4,
            "Muito interessada": 5
        }
        df["interesse_stem_antes"] = (
            df["interesse_stem_antes_category"]
            .map(interest_map)
            .astype(int)
        )

        df["crescimento_interesse_percentual"] = (
            (df["interesse_stem_pos"] - df["interesse_stem_antes"]) * 20
        )
        
        return df
    
    def _get_students_with_interest_growth(self, df:pd.DataFrame):
        df["cresceu_interesse"] = (
            df["crescimento_interesse_percentual"] > 0
        )
        
        return df
    
    def _generate_quality_coefficient(self, df:pd.DataFrame):
        df["coeficiente_de_qualidade"] = (
            (df["aplicabilidade_conhecimento"] + df["relevancia_tema"]) / 2
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
        
        return df
    
    def _find_students_interested_in_stem_careers(self, df:pd.DataFrame):
        df["tem_interesse_em_stem"] = (
            df["interesse_stem_pos"] > 3
        )
        return df
    
    def _get_experienced_and_beginner_participants(self, df:pd.DataFrame):
        map_bool = {
            "Sim": True,
            "Não": False
        }

        df["participacao_previa_stem"] = (
            df["participacao_previa_stem_category"]
            .map(map_bool)
            .astype(bool)
        )
        return df
    
    def _transform_high_school_year(self, df:pd.DataFrame):
        df["ano_ensino_medio"] = (
            df["ano_ensino_medio"]
            .astype(str)
            .str.extract(r"(\d+)", expand=False)
            .astype("Int64")
        )
        
        return df
        
    def _group_by_programs(self,df:pd.DataFrame):
        df["data"] = df["datahora"].dt.date
        grouped_programs_df = df.groupby("data").size().reset_index(name="qtd_participantes")
        
        return df, grouped_programs_df
        
    
    def _drop_unused_columns(self,df: pd.DataFrame):
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
        "relevancia_tema",
        "clareza_explicacoes",
        "compreensao_pixel_algoritmos",
        "nivel_atividades",
        "interesse_stem_pos",
        "interesse_carreira_stem",
        "aplicabilidade_conhecimento",
        "space",
        "space",
        "space",
        "nota_recomendacao",
        "nps_oficina"
        ]
        return df