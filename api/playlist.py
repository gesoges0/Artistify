import json
from collections import defaultdict
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path

import requests

from api.spotify import Spotify


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

    def create_playlist_tracks_by_artist(self):
        access_token = self.outh()
        tracks_by_artist = _get_tracks_by_artist(self.playlist_id)
        for artist, tracks in tracks_by_artist.items():
            # make playlist
            playlist_response = requests.post(
                url=f"https://api.spotify.com/v1/users/{self.playlist_response_model.owner.id}/playlists",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/json",
                },
                json={
                    "name": f"{artist.name} from {self.playlist_response_model.name}",
                    "description": f"{artist.name}'s songs in {self.playlist_response_model.name} playlist",
                    "public": True,  # public ?
                },
            )
            # add tracks
            track_response = requests.post(
                url=f"https://api.spotify.com/v1/playlists/{playlist_response.json()['id']}/tracks",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/json",
                },
                json={"uris": [track.uri for track in tracks]},
            )


@dataclass(frozen=True)
class PlaylistModel:
    name: str
    total_tracks: int
    tracks: list["Track"]
    owner: "Owner"

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
                owner=Owner.from_dict(response["owner"]),
            )
        else:
            raise Exception(f"Unknown playlist response: {response}")


@dataclass(frozen=True)
class Owner:
    display_name: str
    id: str
    uri: str

    @classmethod
    def from_dict(cls, d):
        return cls(d["display_name"], d["id"], d["uri"])


@dataclass(frozen=True)
class Artist:
    name: str
    id: str
    uri: str
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
            uri=d["uri"],
            external_url=d["external_urls"]["spotify"],
        )


@dataclass(frozen=True)
class Track:
    name: str
    id: str
    uri: str
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
            id=track_dict["track"]["id"],
            uri=track_dict["track"]["uri"],
            artists=[
                Artist.from_dict(artist_dict)
                for artist_dict in track_dict["track"]["artists"]
            ],
        )


def show_tracks(playlist_id: str):
    """(アーティスト, 楽曲)一覧を返す"""
    playlist: Playlist = Playlist(playlist_id)

    for track in playlist.playlist_response_model.tracks:
        print("-" * 50)
        print(f"track: {track.name}")
        print(f'artists: {", ".join([artist.name for artist in track.artists])}')


def _get_playlist(playlist_id: str) -> Playlist:
    return Playlist(playlist_id=playlist_id)


def _get_tracks_by_artist(playlist_id: str) -> dict[Artist, list[Track]]:
    """{アーティスト: {楽曲1, 楽曲2, ...}}のマップを返す
    ただし, 楽曲1に対してアーティストが複数いる場合は, {アーティストA: {楽曲1}, アーティストB: {楽曲1}}となる.
    """
    playlist = _get_playlist(playlist_id=playlist_id)

    tracks_by_artist = defaultdict(list)

    for track in playlist.playlist_response_model.tracks:
        for artist in track.artists:
            tracks_by_artist[artist].append(track)

    return tracks_by_artist


def _get_added_by(playlist_id: str) -> Owner:
    playlist = _get_playlist(playlist_id=playlist_id)
    return playlist.playlist_response_model.owner


def output_tracks_by_artist(
    playlist_id: str, output_path: Path, attr: str | None
) -> None:
    tracks_by_artist: dict[Artist, list[Track]] = _get_tracks_by_artist(
        playlist_id=playlist_id
    )
    user_id: str = _get_added_by(playlist_id=playlist_id).id

    if attr:
        available_attrs = {
            field.name for field in Track.__dataclass_fields__.values()
        } & {field.name for field in Artist.__dataclass_fields__.values()}
        assert attr in available_attrs, f"attr must be in {available_attrs}"

    artist_attr, track_attr = (attr, attr) if attr else ("name", "id")

    # TODO: option
    # ---------------------------------
    # ---------------------------------

    output_obj = {
        "playlist": {
            getattr(artist, artist_attr): [
                getattr(track, track_attr) for track in tracks
            ]
            for artist, tracks in tracks_by_artist.items()
        },
        "owner": user_id,
    }

    with open(output_path, "w") as output:
        json.dump(output_obj, output)


def create_each_artist_playlist(playlist_id):
    playlist = _get_playlist(playlist_id=playlist_id)
    playlist.create_playlist_tracks_by_artist()
