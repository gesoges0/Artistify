from api.spotify import Spotify
import requests
from functools import cached_property
from dataclasses import dataclass


class Playlist(Spotify):
    def __init__(self, playlist_id: str):
        self.playlist_id = playlist_id

    @property
    def request_headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.access_token}"}

    @property
    def playlist_url(self) -> str:
        return f"https://api.spotify.com/v1/playlists/{self.playlist_id}"

    @cached_property
    def playlist_response(self):
        """プレイリストの情報を返す(SpotifyのAPIのレスポンスをJSONパースしてるだけの情報)"""
        playlist_response = requests.get(
            self.playlist_url, headers=self.request_headers
        )
        return playlist_response.json()

    @cached_property
    def playlist_response_model(self) -> "PlaylistModel":
        return PlaylistModel.from_playlist_response(self.playlist_response)


@dataclass(frozen=True)
class PlaylistModel:
    name: str
    total_tracks: int
    tracks: list["Track"]

    @classmethod
    def from_playlist_response(cls, response: dict):
        if "tracks" in response and "items" in response["tracks"]:
            return cls(
                name=response["name"],
                total_tracks=response["tracks"]["total"],
                tracks=[
                    Track.from_track_dict(track_dict)
                    for track_dict in response["tracks"]["items"]
                ],
            )
        else:
            raise Exception(f"Unknown playlist response: {response}")


@dataclass(frozen=True)
class Artist:
    name: str
    id: str
    external_url: str

    @classmethod
    def from_dict(cls, d: dict):
        """
        'external_urls': {'spotify': 'https://open.spotify.com/artist/7sfl4Xt5KmfyDs2T3SVSMK'},
        'href': 'https://api.spotify.com/v1/artists/7sfl4Xt5KmfyDs2T3SVSMK',
        'id': '7sfl4Xt5KmfyDs2T3SVSMK',
        'name': 'Lil Jon',
        'type': 'artist',
        'uri': 'spotify:artist:7sfl4Xt5KmfyDs2T3SVSMK'
        """
        return cls(
            name=d["name"],
            id=d["id"],
            external_url=d["external_urls"]["spotify"],
        )


@dataclass(frozen=True)
class Track:
    name: str
    artists: list[Artist]

    @classmethod
    def from_track_dict(cls, track_dict: dict):
        """_summary_
        {
            'added_at': '2024-02-05T15:10:28Z',
            'added_by':
                {
                    'external_urls': {'spotify': 'https://open.spotify.com/user/llc1xxsoknqgh69956sifvyi5'},
                    'id': 'llc1xxsoknqgh69956sifvyi5',
                    'type': 'user',
                    'uri': 'spotify:user:llc1xxsoknqgh69956sifvyi5'
                },
            'track':
                {
                    'album':
                        {
                            'album_type': 'album',
                            'artists':
                                [
                                    {
                                        'external_urls':
                                            {
                                                'spotify': 'https://open.spotify.com/artist/23zg3TcAtWQy7J6upgbUnj'
                                            },
                                        'href': 'https://api.spotify.com/v1/artists/23zg3TcAtWQy7J6upgbUnj',
                                        'id': '23zg3TcAtWQy7J6upgbUnj',
                                        'name': 'USHER',
                                        'type': 'artist',
                                        'uri': 'spotify:artist:23zg3TcAtWQy7J6upgbUnj'
                                    }
                                ],
                            'available_markets': ['AR', ... 'XK'],
                            'external_urls':
                                {
                                    'spotify': 'https://open.spotify.com/album/1RM6MGv6bcl6NrAG8PGoZk'
                                },
                            'href': 'https://api.spotify.com/v1/albums/1RM6MGv6bcl6NrAG8PGoZk',
                            'id': '1RM6MGv6bcl6NrAG8PGoZk',
                            'images':
                                [
                                    {
                                        'height': 640,
                                        'url': 'https://i.scdn.co/image/ab67616d0000b273365b3fb800c19f7ff72602da',
                                        'width': 640
                                    },
                                    {
                                        'height': 300,
                                        'url': 'https://i.scdn.co/image/ab67616d00001e02365b3fb800c19f7ff72602da',
                                        'width': 300
                                    },
                                    {
                                        'height': 64,
                                        'url': 'https://i.scdn.co/image/ab67616d00004851365b3fb800c19f7ff72602da',
                                        'width': 64
                                    }
                                ],
                            'name': 'Confessions (Expanded Edition)',
                            'release_date': '2004-03-23',
                            'release_date_precision': 'day',
                            'total_tracks': 21,
                            'type': 'album',
                            'uri': 'spotify:album:1RM6MGv6bcl6NrAG8PGoZk'
                        },
                    'artists':
                        [
                            {
                                'external_urls': {'spotify': 'https://open.spotify.com/artist/23zg3TcAtWQy7J6upgbUnj'},
                                'href': 'https://api.spotify.com/v1/artists/23zg3TcAtWQy7J6upgbUnj',
                                'id': '23zg3TcAtWQy7J6upgbUnj',
                                'name': 'USHER',
                                'type': 'artist',
                                'uri': 'spotify:artist:23zg3TcAtWQy7J6upgbUnj'
                            },
                            {
                                'external_urls': {'spotify': 'https://open.spotify.com/artist/7sfl4Xt5KmfyDs2T3SVSMK'},
                                'href': 'https://api.spotify.com/v1/artists/7sfl4Xt5KmfyDs2T3SVSMK',
                                'id': '7sfl4Xt5KmfyDs2T3SVSMK',
                                'name': 'Lil Jon',
                                'type': 'artist',
                                'uri': 'spotify:artist:7sfl4Xt5KmfyDs2T3SVSMK'
                            },
                            {
                                'external_urls': {'spotify': 'https://open.spotify.com/artist/3ipn9JLAPI5GUEo4y4jcoi'},
                                'href': 'https://api.spotify.com/v1/artists/3ipn9JLAPI5GUEo4y4jcoi',
                                'id': '3ipn9JLAPI5GUEo4y4jcoi',
                                'name': 'Ludacris',
                                'type': 'artist',
                                'uri': 'spotify:artist:3ipn9JLAPI5GUEo4y4jcoi'
                            }
                        ],
                    'available_markets': ['AR', ... , 'XK'],
                    'disc_number': 1,
                    'duration_ms': 250373,
                    'episode': False,
                    'explicit': False,
                    'external_ids': {'isrc': 'USAR10301423'},
                    'external_urls': {'spotify': 'https://open.spotify.com/track/5rb9QrpfcKFHM1EUbSIurX'},
                    'href': 'https://api.spotify.com/v1/tracks/5rb9QrpfcKFHM1EUbSIurX',
                    'id': '5rb9QrpfcKFHM1EUbSIurX',
                    'is_local': False,
                    'name': 'Yeah! (feat. Lil Jon & Ludacris)',
                    'popularity': 87,
                    'track': True,
                    'track_number': 2,
                    'type': 'track',
                    'uri': 'spotify:track:5rb9QrpfcKFHM1EUbSIurX'
                },
                'video_thumbnail': {'url': None}}
        """
        return cls(
            name=track_dict["track"]["name"],
            artists=[
                Artist.from_dict(artist_dict)
                for artist_dict in track_dict["track"]["artists"]
            ],
        )


def show_songs_and_artists(playlist_id: str):
    """(アーティスト, 楽曲)一覧を返す"""
    playlist: Playlist = Playlist(playlist_id)

    for track in playlist.playlist_response_model.tracks:
        print("-" * 50)
        print(f"track: {track.name}")
        print(f'artists: {", ".join([artist.name for artist in track.artists])}')


def get_songs_by_artist_dict(playlist_id: str):
    """{アーティスト: {楽曲1, 楽曲2, ...}}のマップを返す
    ただし, 楽曲1に対してアーティストが複数いる場合は, {アーティストA: {楽曲1}, アーティストB: {楽曲1}}となる.
    """
    pass
