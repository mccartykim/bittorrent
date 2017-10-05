#!/usr/bin/python3
from bencode import encode, Parser
import logging
# using the blocking requests library for now, but will try to plop in aiohttp later
import requests
import random
import string


# for now, I think I'll just parse the torrent file again as necessary, seeking what data I need on a provisional basis
# def read_torrent(path):
#     p = Parser()
#     metadata = None
#     with open(path, "rb") as f:
#         metadata = p.parse(f.read())
#     if metadata is None:
#         raise(ValueError())
#     pieces = []
#     piece_length = metadata[b"info"][b"piece length"]
#     raw_pieces = metadata[b"info"][b"pieces"]
#     piece_hashes = [raw_pieces[x:x+20] for x in range(0, len(raw_pieces), 20)]
#     length =  metadata[b"info"].get(b"length")
#     if not length: 
#         files = metadata[b"info"].get(b"files")
#         # GO TO YOUR ROOM AND THINK LONG AND HARD ABOUT FILES
#         root_dir = metadata[b"name"]
#         # TODO read about python's internal objects for paths
#     else:
#         filename = metadata[b"name"]
        
    
def tracker_get(path):
    p = Parser()
    metadata = None
    with open(path, "rb") as f:
        metadata = p.parse(f.read())
    if metadata is None:
        raise(ValueError())
    pieces = []
    piece_length = metadata[b"info"][b"piece length"]
    raw_pieces = metadata[b"info"][b"pieces"]
    piece_hashes = [raw_pieces[x:x+20] for x in range(0, len(raw_pieces), 20)]
    length =  metadata[b"info"].get(b"length")
    if not length: 
        files = metadata[b"info"].get(b"files")
        # GO TO YOUR ROOM AND THINK LONG AND HARD ABOUT FILES
        root_dir = metadata[b"name"]
        # TODO read about python's internal objects for paths
    #else:
    #    filename = metadata[b"name"]
    params = {"info_hash": p.get_info_hash(dict_=metadata),
            "peer_id": "".join(random.choice(string.ascii_lowercase) for i in range(20)), # FIXME add a smarter system for random peerid, or at least something alluding to this client's name, which is... SOME KIND OF BITTORRENT?!
            # "ip": "127.0.0.1" # but a real ip ya dingus
            "port": 6881, # I don't know if this will work with our firewall, but I'll give it a shot, then pick a weirder port
            "uploaded": 0,
            "downloaded": 0,
            "left": "0", # Look, I realize the length remaining is derived, especially for multiple files, and I want this to work now.  FIXME
            # "event": "started",
            "compact": 1, # mandatory on many servers
            }
    r = requests.get(metadata[b"announce"], params=params)
    # print(r.content)
    print(r.text)
    print(p.parse(r.content))


if __name__=="__main__":
    tracker_get("../sample.torrent")
