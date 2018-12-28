import os
import json
import logging


def check_cache(username):
    """
    Check for cache on the environment variables.
    If it exists, write the cache to disk
    if it does not exist there already.
    :return: -
    """

    filename = f'.cache-{username}'

    if 'SPOTIPY_CACHE' in os.environ:
        logging.info('Found cache in env variables')

        cache = os.environ.get('SPOTIPY_CACHE')

        with open(filename, 'w') as fh:
            logging.info('Dumped cache to {}'.format(filename))
            fh.write(cache)


def get_playlist_tracks(sp, username, playlist_id):
    '''

    Get all the tracks in a users playlist.

    Concatenates tracks for playlists longer than 100 tracks.

    :param username:
    :param playlist_id:
    :return:
    '''

    results = sp.user_playlist_tracks(username, playlist_id)
    tracks = results['items']

    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])

    return tracks


def prompt_for_playlist(playlists):
    playlists_dict = {}
    for i, item in enumerate(playlists['items']):
        playlists_dict[i] = item['name']
        print('[{}]\t{}'.format(i, item['name']))

    chosen_playlist = False
    while not chosen_playlist:
        i = int(input('SELECT A DESTINATION PLAYLIST: '))
        chosen_playlist = playlists_dict[i]

    return chosen_playlist


def get_dest_playlist_id(playlist_name: str, playlists: list):
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
