import os
import sys
import time
import logging
import spotipy
import spotipy.util as sputil
import utils as util

from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)


def main():
    username = os.environ.get('SPOTIPY_USERNAME')
    playlist_name = os.environ.get("SPOTIPY_PLAYLIST")

    assert username is not None, 'username not found in env variables'
    assert playlist_name is not None, 'playlist not found in env variables'

    util.check_cache(username)

    # TODO: review bare minimum scope
    scope = 'playlist-modify playlist-modify-public user-library-read playlist-modify-private'

    token = sputil.prompt_for_user_token(username, scope=scope)

    if not token:
        raise ValueError('Authorization Failed')

    sp = spotipy.Spotify(auth=token)

    # Get user playlists
    playlists = sp.user_playlists(username)

    # Get destination playlist id
    dest_playlist_id = util.get_dest_playlist_id(playlist_name, playlists)

    # Get discover weekly track IDs
    dw_id = util.get_dw_id(playlists)
    dw_tracks_info = sp.user_playlist_tracks(username, dw_id)
    dw_tracks = dw_tracks_info['items']

    dw_track_ids = util.tracks_to_ids(dw_tracks)

    while True:
        # Get the tracks in destination playlist
        # TODO - update to get all tracks using:
        #         dest_playlist_tracks = util.get_playlist_tracks(sp, username, dest_playlist_id)
        dest_playlist_tracks = util.get_playlist_tracks(sp, username, dest_playlist_id)
        dest_track_ids = util.tracks_to_ids(dest_playlist_tracks)

        # Check which tracks are saved in user library
        is_saved = sp.current_user_saved_tracks_contains(tracks=dw_track_ids)
        saved_tracks = [d for i, d in enumerate(dw_track_ids) if is_saved[i]]

        # Get which tracks to add to playlist
        tracks_to_add = [t for t in saved_tracks if t not in dest_track_ids]

        if tracks_to_add:
            logging.info('Adding {} tracks to {}'.format(len(tracks_to_add), playlist_name))
            sp.user_playlist_add_tracks(username, dest_playlist_id, tracks_to_add)
        else:
            logging.info('No new liked tracks found.')

        # Sleep for 1 second
        time.sleep(1)


if __name__ == '__main__':
    load_dotenv()
    main()
