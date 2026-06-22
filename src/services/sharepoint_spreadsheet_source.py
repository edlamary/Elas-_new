import os
import tempfile
from pathlib import Path

import msal
import requests
from dotenv import load_dotenv

load_dotenv()


class SharePointSpreadsheetSource:
    """Baixa um .xlsx do SharePoint via MSAL (ROPC) e retorna o Path para uso na pipeline."""

    def __init__(self):
        self._sharepoint_url = os.environ["SHAREPOINT_URL"].rstrip("/")
        self._tenant = os.environ["SHAREPOINT_TENANT"]
        self._client_id = os.environ["SHAREPOINT_CLIENT_ID"]
        self._username = os.environ["SHAREPOINT_USER"]
        self._password = os.environ["SHAREPOINT_PASS"]
        self._file_path = os.environ["FILE_PATH"]

        sharepoint_host = "/".join(self._sharepoint_url.split("/")[:3])
        self._scopes = [f"{sharepoint_host}/.default"]

    def fetch(self) -> Path:
        token = self._get_access_token()
        xlsx_bytes = self._download_xlsx_bytes(token)

        tmp = tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False)
        tmp.write(xlsx_bytes)
        tmp.close()

        return Path(tmp.name)

    def _get_access_token(self) -> str:
        app = msal.PublicClientApplication(
            self._client_id,
            authority=f"https://login.microsoftonline.com/{self._tenant}",
        )
        result = app.acquire_token_by_username_password(
            username=self._username,
            password=self._password,
            scopes=self._scopes,
        )
        if "access_token" not in result:
            error = result.get("error_description") or result.get("error")
            raise RuntimeError(f"Falha na autenticação: {error}")
        return result["access_token"]

    def _download_xlsx_bytes(self, token: str) -> bytes:
        encoded_path = requests.utils.quote(self._file_path)
        url = f"{self._sharepoint_url}/_api/web/GetFileByServerRelativeUrl('{encoded_path}')/$value"
        response = requests.get(url, headers={"Authorization": f"Bearer {token}"}, stream=True)
        response.raise_for_status()
        return response.content
