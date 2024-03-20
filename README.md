# Artistify



## Usage

### .env file
```plaintext
CLIENT_ID=xxxxxxxxxx
CLIENT_SECRET=xxxxxxxxxx
PLAYLIST_ID=xxxxxxxxxx
```


### usage of each api

#### show_songs_and_artists_in_playlist
show (song, list of artists) in a playlist
```
$ python main.py show-songs-and-artists-in-playlist 6CpQWdViAFjjnXCEudZVQR
Getting playlist info for ID: 6CpQWdViAFjjnXCEudZVQR
--------------------------------------------------
track: Elastic Heart
artists: Sia
--------------------------------------------------
track: Rainbow
artists: Sia
--------------------------------------------------
track: Sugar (feat. Francesco Yates)
artists: Robin Schulz, Francesco Yates
--------------------------------------------------
track: Titanium (feat. Sia)
artists: David Guetta, Sia
--------------------------------------------------
track: Dusk Till Dawn (feat. Sia) - Radio Edit
artists: ZAYN, Sia
--------------------------------------------------
track: Yellow
artists: Coldplay
--------------------------------------------------
track: Adventure of a Lifetime
artists: Coldplay
--------------------------------------------------
track: Shape of My Heart
artists: Backstreet Boys
```
