# API Key: 630a67efa81819f816483ae706932202
# Shared Secret: 011f1c67ae96efa46fdeb854dad3950c

import pylast
	
API_KEY = "630a67efa81819f816483ae706932202"
API_SECRET = "011f1c67ae96efa46fdeb854dad3950c"

# Type help(pylast.LastFMNetwork) or help(pylast) in a Python interpreter
# to get more help about anything and see examples of how it works
# https://www.last.fm/api


def get_network(username, password_hash=None):
    # In order to perform a write operation you need to authenticate yourself
    # password_hash = pylast.md5(PASSWORD)
    if password_hash:
        return pylast.LastFMNetwork(
            api_key=API_KEY,
            api_secret=API_KEY,
            username=username,
            password_hash=password_hash,
        )
    return pylast.LastFMNetwork(
        api_key=API_KEY,
        api_secret=API_KEY,
        username=username,
    )


