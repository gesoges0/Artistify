import os
from dataclasses import dataclass
from functools import cached_property

import requests
from dotenv import load_dotenv

# .envファイルから環境変数をロード
load_dotenv()


class Spotify:
    # .envファイルからクライアントIDとクライアントシークレットを取得
    _client_id: str
    _client_secret: str

    # Spotify APIのトークン取得エンドポイント
    token_url = "https://accounts.spotify.com/api/token"

    @property
    def client_id(self) -> str | None:
        return os.getenv("CLIENT_ID")

    @property
    def client_secret(self) -> str | None:
        return os.getenv("CLIENT_SECRET")

    @property
    def token_data(self) -> dict[str, str | None]:
        return {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }

    @cached_property
    def access_token(self):
        token_response = requests.post(self.token_url, data=self.token_data)
        access_token = token_response.json()["access_token"]
        return access_token
