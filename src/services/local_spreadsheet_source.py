from pathlib import Path


class LocalSpreadsheetSource:
    def fetch(self) -> Path:
        return Path(r"C:\TI\Codes\ellas\src\data\Formulário de feeback oficina (respostas).xlsx")