#! /usr/bin/python3
from bencode import Parser

class PeerMessager(object):
    def __init__(self, infohash, tracker_url, peer_id, peers=[]):
        self.infohash = infohash
        self.tracker_url = tracker_url
        self.peers = peers
        self.peer_id = peer_id
        self.pieces = []


    def handshake(self, peer):
        inital = "19BitTorrent protocol" 
        blanks = b'\x00'*8
        # TODO raw infohash
        # TODO if raw infohashes not equal, sever
        # TODO send peer id as 20 byte string


    def keepalive(self):
        pass


    def choke(self, peer):
        pass


    def unchoke(self, peer):
        pass
    

    def interested(self, peer):
        pass


    def not_interested(self, peer):
        pass
    

    def have(self, peer, piece_index):
        pass


    def bitfield(self, peer):
        pass


    def request(self, peer, piece_index):
        pass


    def piece(self, peer, piece_index, begin):
        pass

    
    def cancel(self, peer, begin, length):
        pass
