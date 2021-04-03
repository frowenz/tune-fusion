# API Key: 630a67efa81819f816483ae706932202
# Shared Secret: 011f1c67ae96efa46fdeb854dad3950c

import pylast
	
API_KEY = "630a67efa81819f816483ae706932202"
API_SECRET = "011f1c67ae96efa46fdeb854dad3950c"
USERNAME = "lynmarie44"
PASSWORD = ""

# Type help(pylast.LastFMNetwork) or help(pylast) in a Python interpreter
# to get more help about anything and see examples of how it works


if __name__  == "__main__":

    # In order to perform a write operation you need to authenticate yourself
    # password_hash = pylast.md5(PASSWORD)
    # print(password_hash)

    network = pylast.LastFMNetwork(
        api_key=API_KEY,
        api_secret=API_SECRET,
        username=USERNAME,
        # password_hash=password_hash,
    )

    name = input("last.fm username: ")
    usr = network.get_user(name)
    top_tracks = usr.get_top_tracks(period=pylast.PERIOD_12MONTHS)
    n = min(10, len(top_tracks))

    print(f"{name}'s top 10 tracks:")
    for i in range(n):
        print(f"{i+1:2d}: {top_tracks[i].item}")
