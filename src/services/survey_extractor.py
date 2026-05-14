from pathlib import Path
import pandas as pd
from services.base_spreadsheet_extractor import BaseSpreadsheetExtractor

class SurveyExtractor(BaseSpreadsheetExtractor):
  def __init__(self) -> None:
    ...
  
  def extract(self, path:Path) -> pd.DataFrame:
    df = super().extract(path)


    df["carimbo_de_datahora"] = pd.to_datetime(
            df["carimbo_de_datahora"]
    )
    
    df = df.astype({
    "qual_a_sua_idade": int,
    "em_qual_ano_do_ensino_medio_voce_esta": "category",
    "antes_da_oficina_como_voce_classificaria_seu_interesse_por_areas_de_stem_ciencia_tecnologia_engenharia_e_matematica": "category",
    "voce_ja_participou_de_alguma_outra_atividade_curso_ou_oficina_relacionada_a_areas_de_stem_antes_desta": "category",
    "qual_area_de_estudo_ou_carreira_voce_esta_considerando_para_o_futuro": "category",
    "em_uma_escala_de_1_a_5_como_voce_avalia_a_relevancia_dos_temas_abordados_na_oficina_para_o_seu_interesse_pessoal": int,
    "em_uma_escala_de_1_a_5_como_voce_avalia_a_clareza_das_explicacoes_dadas_durante_a_oficina": int,
    "em_uma_escala_de_1_a_5_como_voce_avalia_a_sua_compreensao_sobre_o_tema_pixel_e_algoritmos_apos_a_oficina": int,
    "qual_foi_o_nivel_das_atividades": "category",
    "apos_participar_da_oficina_o_quanto_seu_interesse_por_areas_de_stem_ciencia_tecnologia_engenharia_e_matematica_aumentou_1_a_5": int,
    "apos_participar_da_oficina_voce_considera_seguir_uma_carreira_em_alguma_area_de_stem": int,
    "em_uma_escala_de_1_a_5_quao_aplicaveis_voce_considera_os_conhecimentos_adquiridos_nesta_oficina_para_o_seu_futuro_academico_ou_profissional": int,
    "o_que_voce_mais_gostou_na_oficina": str,
    "de_que_forma_a_oficina_influenciou_sua_percepcao_sobre_as_areas_de_stem": str,
    "como_voce_acha_que_podemos_melhorar": str,
    "tem_algum_comentario_adicional_ou_sugestao_sobre_as_oficinas": str,
    "em_uma_escala_de_0_a_10_o_quanto_voce_recomendaria_esta_oficina_a_uma_amiga_interessada_em_stem": int,
    })
    
    debug_path = Path("src/debug/raw_df.xlsx")
    df.to_excel(debug_path, index=False)
        
    return df