import sys
import spotipy
import spotipy.util as util

from pprint import pprint

# User ID = renierbotha
username = sys.argv[1]
scope = 'playlist-modify-private'

token = util.prompt_for_user_token(username, scope=scope)

if token:

    sp = spotipy.Spotify(auth=token)

    dw_id = None

    playlists = sp.user_playlists(username)
    for item in playlists['items'][:10]:
        if item['name'] == 'Discover Weekly':
            dw_id = item['id']

    if not dw_id:
        raise ValueError('Discover Weekly ID could not be found - make sure to set it to public')

    dw_tracks = sp.user_playlist_tracks(username, dw_id)

    pprint(dw_tracks['items'][0])


    sp.current_user_saved_tracks_contains()


else:
    print('Authorization failed')
