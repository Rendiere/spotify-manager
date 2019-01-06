import os
import sys
import json
import time
import logging
import spotipy
import spotipy.util as sputil
import utils as util

from pprint import pprint


def setup_spotipy():
    username = os.environ.get('SPOTIPY_USERNAME')

    scope = 'playlist-modify playlist-modify-public user-library-read playlist-modify-private'

    token = sputil.prompt_for_user_token(username, scope=scope)

    sp = spotipy.Spotify(auth=token)

    return sp

def dw_tracks_fixture():

    pass



if __name__ == '__main__':

    dest_playlist = os.environ.get('SPOTIPY_PLAYLIST')

    sp = setup_spotipy()



