#! /usr/bin/python3
from bencode import Parser
import asyncio

class PeerMessager(object):
    def __init__(self, infohash, tracker_url, peer_id, peers=[]):
        self.infohash = infohash
        self.tracker_url = tracker_url
        self.peers = peers
        self.peer_id = peer_id
        self.pieces = []
        self.loop = asyncio.get_event_loop()

    # TODO shared object to manage piece state...

    async def start_connection(self, peer_id, peer):
        reader, writer = await asyncio.open_connection(peer(0), peer(1), loop=self.loop)
        self.handshake(peer_id, reader, writer)
        # TODO spawn task to handle communications
        

    # NOTE consider connection object for each peer?
    async def handshake(self, peer_id, reader, writer):
        inital = b"19BitTorrent protocol" 
        await writer.write(inital)
        blanks = b'\x00'*8
        await self.write_prefixed(blanks, writer)
        infohash = self.infohash
        await self.write_prefixed(infohash, writer)
        await self.write_prefixed(self.peer_id, writer)
        return True

    async def write_prefixed(self, bs, writer):
        return writer.write(self.len_prefix(bs))

    @staticmethod
    def len_prefix(bs):
        p = str(len(bs))
        return p + bs


    async def keepalive(self, writer):
        return b"0"

    async def choke(self, writer):
        return b"1\0"
        
    async def unchoke(self, writer):
        return b"1\0"
    

    async def interested(self, writer):
        pass


    async def not_interested(self, writer):
        pass
    

    async def have(self, peer, piece_index, writer):
        pass


    # TODO figure out what exactly bitfield is :-(
    async def bitfield(self, peer, writer):
        pass


    async def request(self, peer, piece_index, begin, length, writer):
        pass


    async def piece(self, peer, piece_index, begin, writer):
        pass

    
    async def cancel(self, peer, index, begin, length, writer):
        pass
