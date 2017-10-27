#! /usr/bin/python3
"""BitTorrent Client
By Kimberly McCarty
It's for fun, okay?"""

import bencode
import read_torrent
import peer_messaging
import asyncio

# FIXME STUB
async def dispatcher():
    # create connections to peers
    # and download random pieces
    pass

class PieceManager(object):
    def __init__(self, piece_hashes, piece_status=None, piece_length, file_data):
        self.hashes = list(piece_hashes)
        # pieces can have three states
        # unstarted, partial, or finished
        # In order to minimize complexity from noncontiguous dls on the piece level, 
        # I plan on focusing on downloading each piece in sequential chunks
        # That way, I just track how much of the piece has been downloaded
        # and derive the next index from that
        self.piece_length = piece_length
        self.piece_status = piece_status or [0 for _ in range(len(piece_hashes))]
        self.file_data = file_data

    def is_complete(self, piece_index):
        # STUB FIXME: Sample data from file(s)
        # And hash the bytestring equivalnet
        pass

    def find_data(self, byte_index, length):
        # STUB FIXME
        # Find bytes from the appropriate files given the index in the torrent file
        pass

    def write_data(self, byte_index, bytestring):
        # STUB FIXME
        # write a string of binary bytes to the appropriate file
        pass
    

def allocate_files(files):
    for file in files:
        allocate_file(*file)

def allocate_file(path, length):
    with open(path, "wb") as f:
        f.seek(length - 1)
        f.write(b"\x00")

def write_chunk(index, data):
    """Given an index in bytes, and a bytestring, write to appropriate file"""

def main(torrent_file_path):
    metadata = read_torrent.tracker_get(torrent_file_path)
    files = []
    if not metadata[b'info'].get(b'length'):
        for f in metadata[b"files"]:
            ftuple = (f[b"path"], f[b"length"])
            files.append(ftuple)
    else:
        ftuple = (metadata[b"info"][b"name"], f[b"info"][b"length"])
        files.append(ftuple)
    allocate_files(files)
    # TODO system to account for pieces
    messenger = peer_messaging.PeerMessager(metadata, metadata[b'infohash'])
    