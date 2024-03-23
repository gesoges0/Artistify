import os
from pathlib import Path

import click

from api.playlist import output_tracks_by_artist, show_tracks


@click.group()
def cli():
    pass


@cli.command()
@click.argument("playlist_id")
def show_tracks_in_playlist(playlist_id: str):
    """Get information about a playlist."""
    click.echo(f"Getting playlist info for ID: {playlist_id}")
    show_tracks(playlist_id)


@cli.command()
@click.argument("playlist_id")
@click.argument("output_path")
@click.argument("attr", default="id")
def output_tracks_by_artist_in_playlist(playlist_id: str, output_path: str, attr: str):
    """Get information about an artist."""
    click.echo(f"Getting playlist info for ID: {playlist_id}")
    output_tracks_by_artist(playlist_id, Path(output_path), attr)


if __name__ == "__main__":
    cli()
