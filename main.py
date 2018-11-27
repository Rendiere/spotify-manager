import sys
import spotipy
import spotipy.util as util

if __name__ == '__main__':
    username = sys.argv[1]
    scope = 'playlist-modify-private user-library-read'

    token = util.prompt_for_user_token(username, scope=scope)

    if token:

        sp = spotipy.Spotify(auth=token)

        dw_id = None

        # Get user playlists
        playlists = sp.user_playlists(username)

        for item in playlists['items']:
            if item['name'] == 'Discover Weekly':
                dw_id = item['id']

        if not dw_id:
            raise ValueError('Discover Weekly ID could not be found - make sure to set it to public')

        # Get discover weekly tracks
        dw_tracks = sp.user_playlist_tracks(username, dw_id)

        # Get discover weekly track IDs
        dw_track_ids = [item['track']['id'] for item in dw_tracks['items']]

        # Check which tracks are saved in user library
        is_saved = sp.current_user_saved_tracks_contains(tracks=dw_track_ids)

        # For each track that is saved, try adding to desired playlist

    else:
        print('Authorization failed')
