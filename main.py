import sys
import spotipy
import spotipy.util as util


def prompt_for_playlist(playlists):
    playlists_dict = {}
    for i, item in enumerate(playlists['items']):
        playlists_dict[i] = item['name']
        print('[{}]\t{}'.format(i, item['name']))

    print('')
    chosen_playlist = False
    while not chosen_playlist:
        i = int(input('SELECT A DESTINATION PLAYLIST: '))
        chosen_playlist = playlists_dict[i]

    return chosen_playlist


def get_dest_playlist_id(playlist_name: str, playlists: list):
    if not playlist_name:
        playlist_name = prompt_for_playlist(playlists)

    # TODO clean this up
    playlist_id = None
    for item in playlists['items']:
        if item['name'] == playlist_name:
            playlist_id = item['id']

    if not playlist_id:
        raise ValueError('Chosen playlist was not found')

    return playlist_id


def get_dw_id(playlists: list):
    '''
    Get discvoer weekly ID
    :param playlists:
    :return: string
    '''
    dw_id = None
    for i, item in enumerate(playlists['items']):
        if item['name'] == 'Discover Weekly':
            dw_id = item['id']

    if not dw_id:
        raise ValueError('Discover Weekly ID could not be found - make sure to set it to public')

    return dw_id


def tracks_to_ids(tracks):
    return [item['track']['id'] for item in tracks['items']]


if __name__ == '__main__':

    username = sys.argv[1]
    if len(sys.argv) > 2:
        playlist_name = sys.argv[2]  # name of playlist to move liked songs to
    else:
        playlist_name = ''

    # TODO: review bare minimum scope
    scope = 'playlist-modify playlist-modify-public user-library-read playlist-modify-private'

    token = util.prompt_for_user_token(username, scope=scope)

    if not token:
        raise ValueError('Authorization Failed')

    sp = spotipy.Spotify(auth=token)

    # Get user playlists
    playlists = sp.user_playlists(username)

    dest_playlist_id = get_dest_playlist_id(playlist_name, playlists)

    # Get the tracks in destination playlist
    dest_playlist_tracks = sp.user_playlist_tracks(username, dest_playlist_id)
    dest_track_ids = tracks_to_ids(dest_playlist_tracks)

    # Prompt user to select playlist
    dw_id = get_dw_id(playlists)

    # Get discover weekly tracks
    dw_tracks = sp.user_playlist_tracks(username, dw_id)

    # Get discover weekly track IDs
    dw_track_ids = tracks_to_ids(dw_tracks)

    # Check which tracks are saved in user library
    is_saved = sp.current_user_saved_tracks_contains(tracks=dw_track_ids)
    saved_tracks = [d for i, d in enumerate(dw_track_ids) if is_saved[i]]

    tracks_to_add = [t for t in saved_tracks if t not in dest_playlist_id]

    print('Adding track to {}'.format(playlist_name))
    sp.user_playlist_add_tracks(username, dest_playlist_id, tracks_to_add)
