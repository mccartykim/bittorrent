#!/usr/bin/python3
from bencode import encode, Parser
import logging
# using the blocking requests library for now, but will try to plop in aiohttp later
import requests
import random
import string
import struct
from ipaddress import IPv4Address


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
    print(metadata[b"announce"])
    r = requests.get(metadata[b"announce"], params=params)
    # print(r.content)
    response = p.parse(r.content)
    print(unpack_peers(response[b'peers']))

def unpack_peers(s):
    # I get a bit cute with list comprehensions here, and I would like to be readable.  Bear with me!
    # First, we slice the data into peer data with six bytes each.  Four for IPv4, two for the port's int
    raw_peers = [s[x:x+6] for x in range(0, len(s), 6)]
    # Then, take each six byte string, and parse each part
    peers = [(IPv4Address(p[0:4]), struct.unpack("!H", p[4:6])[0]) for p in raw_peers]
    # If I was feeling really clever, I could have done this in one operation, but that'd be hard to read and I'm not going for speed.
    return peers

if __name__=="__main__":
    tracker_get("../sample.torrent")
