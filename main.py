import os
import click
from api.artist import get_artist_infos
from api.playlist import show_songs_and_artists


@click.group()
def cli():
    pass


@cli.command()
@click.argument("playlist_id")
def show_songs_and_artists_in_playlist(playlist_id: str):
    """Get information about a playlist."""
    click.echo(f"Getting playlist info for ID: {playlist_id}")
    show_songs_and_artists(playlist_id)


@cli.command()
@click.argument("artist_id")
def get_artist_info(artist_id):
    """Get information about an artist."""
    click.echo(f"Getting artist info for ID: {artist_id}")
    get_artist_infos(artist_id)


if __name__ == "__main__":
    cli()
