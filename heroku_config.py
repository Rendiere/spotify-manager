import os


def split_line(line: str):
    """
    Split a config line into KEY / VALUE parts

    :param line: example: SPOTIPY_CLIENT_ID='...'
    :return: Tuple with (KEY, VALUE)
    """
    line = line.lstrip().rstrip()
    return tuple(line.split(sep='=', maxsplit=1))


def set_config(key_val_pairs: list):
    """
    Set a list key / value pairs on heroku config

    :param key_val_pairs:
    :return: none
    """
    cmd = 'heroku config:set '
    for key, val in key_val_pairs:
        cmd += '{}={} '.format(key, val)
    os.system(cmd)


if __name__ == '__main__':
    with open('.env') as f:
        key_val_pairs = [split_line(line) for line in f]
        set_config(key_val_pairs)
