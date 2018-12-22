import logging


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
