import os
import base64
from dataclasses import dataclass
from functools import cached_property
import urllib.parse

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

    @property
    def client_credentials(self):
        return f"{self.client_id}:{self.client_secret}"

    @property
    def client_credentials_b64(self):
        return base64.b64encode(s=self.client_credentials.encode()).decode()

    @cached_property
    def access_token(self):
        token_response = requests.post(self.token_url, data=self.token_data)
        access_token = token_response.json()["access_token"]
        return access_token

    @property
    def secret_access_token(self):
        token_response = requests.post(
            self.token_url,
            headers={"Authorization": f"Basic {self.client_credentials_b64}"},
            data={"grant_type": "client_credentials"},
        )
        access_token = token_response.json()["access_token"]
        return access_token

    def outh(self):
        redirect_uri = "http://localhost:8887/callback"

        # Spotify authorization urls
        auth_url = "https://accounts.spotify.com/authorize"
        token_url = "https://accounts.spotify.com/api/token"

        # authorization page params
        auth_params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": redirect_uri,
            "scope": "playlist-modify-public",
        }

        # generate authorization url
        auth_url_with_params = auth_url + "?" + urllib.parse.urlencode(auth_params)

        # ------------------------------------------------------------------------------------------------
        # input xxxx from uri ?code=xxxx
        print(
            "Please go to the following URL and authorize access:", auth_url_with_params
        )
        # ------------------------------------------------------------------------------------------------

        # authorization code from user input
        auth_code = input("Enter the authorization code: ")

        # request body for access token
        token_data = {
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": redirect_uri,
        }

        # request headers
        headers = {
            "Authorization": f"Basic {self.client_credentials_b64}",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        # get access token
        token_response = requests.post(token_url, headers=headers, data=token_data)
        token_data = token_response.json()
        access_token = token_data["access_token"]

        return access_token
