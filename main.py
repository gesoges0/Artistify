import os

import requests
from dotenv import load_dotenv

# .envファイルから環境変数をロード
load_dotenv()

# .envファイルからクライアントIDとクライアントシークレットを取得
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# Spotify APIのトークン取得エンドポイント
token_url = "https://accounts.spotify.com/api/token"

# トークン取得リクエストのボディ
token_data = {
    "grant_type": "client_credentials",
    "client_id": client_id,
    "client_secret": client_secret,
}

# トークン取得リクエストの送信
token_response = requests.post(token_url, data=token_data)

# トークンの取得
access_token = token_response.json()["access_token"]

# プレイリスト情報取得エンドポイント
playlist_id = os.getenv("PLAYLIST_ID")  # プレイリストのID
playlist_url = f"https://api.spotify.com/v1/playlists/{playlist_id}"

# プレイリスト情報取得リクエストのヘッダー
playlist_headers = {"Authorization": f"Bearer {access_token}"}

# プレイリスト情報取得リクエストの送信
playlist_response = requests.get(playlist_url, headers=playlist_headers)

# プレイリスト情報の取得
playlist_data = playlist_response.json()

# プレイリスト内の楽曲とアーティストの一覧表示
# print(playlist_data)

if "tracks" in playlist_data and "items" in playlist_data["tracks"]:
    print("Playlist Name:", playlist_data["name"])
    print("Total Tracks:", playlist_data["tracks"]["total"])
    print("Tracks:")
    for item in playlist_data["tracks"]["items"]:
        # track_name = item['track']['name']
        # artists = ", ".join([artist['name'] for artist in item['track']['artists']])
        # print(f"{track_name} // {artists}")
        # print(item)
        exit()
else:
    print("Error: Unable to fetch playlist data.")
