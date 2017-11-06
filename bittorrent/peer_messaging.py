#! /usr/bin/python3
# from bencode import Parser
import asyncio
import struct
import math

"""Let's define a peer object:
Peer
+ writer
+ reader
+ peerid
+ pieces
"""


class Peer(object):
    def __init__(self, peer_tup, metainfo):
        self.address = peer_tup[0]
        self.port = peer_tup[1]
        self.peer_id = None
        self.writer = None
        self.reader = None
        self.pieces = [None] * len(metainfo[b'pieces'])

class PeerMessenger(object):
    def __init__(self, metainfo):
        peers = []
        for peer in metainfo[b'peers']:
            peers.append(Peer(peer, metainfo))
        self.peers = peers
        self.infohash = metainfo[b'infohash']
        self.peer_id = metainfo[b'peer_id']
        self.pieces = []
        self.loop = asyncio.get_event_loop()


    async def start_connection(self, peer_id, peer):
        reader, writer = await asyncio.open_connection(peer(0), peer(1), loop=self.loop)
        peer.writer = writer
        peer.reader = reader
        self.handshake(peer)
        # TODO spawn task to handle communications



    # NOTE consider connection object for each peer?
    async def handshake(self, peer):
        inital = b"\x19BitTorrent protocol" 
        await peer.writer.write(inital)
        blanks = b'\x00'*8
        await peer.writer.write(blanks)
        infohash = self.infohash
        await peer.writer.write(infohash)
        await peer.writer.write(self.peer_id)
        return True

    async def write_prefixed(self, bs, writer):
        return writer.write(self.len_prefix(bs))

    @staticmethod
    def len_prefix(bs):
        p = struct.pack(">l", len(bs))
        return p + bs


    async def keepalive(self, peer):
        self.write_prefixed(b"", peer.writer)

    async def choke(self, peer):
        header = b"\0"
        self.write_prefixed(header, peer.writer)
        
    async def unchoke(self, peer):
        header = b"\x01"
        self.write_prefixed(header, peer.writer)
    

    async def interested(self, peer):
        header = b"\x02"
        self.write_prefixed(header, peer.writer)

    async def not_interested(self, peer):
        header = b"\x03"
        self.write_prefixed(header, peer.writer)
    

    async def have(self, peer, piece_index):
        header = b"\x04"
        index = struct.pack(">l", piece_index)
        self.write_prefixed(header+index, peer.writer)

    async def bitfield(self, peer):
        header = b"\x05"
        #bf = bytearray(math.ceil(len(self.pieces) / 8))
        bf = bytearray()
        for i, status in enumerate(self.pieces):
            if len(bf) < (i//8) + 1:
                bf.append(0x00)
            bf[-1] = bf[-1] | (status << (7-(i % 8)))
        message = header + bf
        self.write_prefixed(message, peer.writer)

    async def request(self, peer, index, begin, length=16384):
        header = b"\x06"
        message = struct.pack(">l", index) + struct.pack(">l", begin) + struct.pack(">l", length)
        self.write_prefixed(header+message, peer.writer)

    async def piece(self, peer, piece_index, begin, piece):
        header = b"\x07"
        message = header + struct.pack(">ll", piece_index, begin) + piece
        self.write_prefixed(message, peer.writer)
    
    async def cancel(self, peer, index, begin, length):
        header = b"\x08"
        message = struct.pack(">l", index) + struct.pack(">l", begin) + struct.pack(">l", length)
        self.write_prefixed(header+message, peer.writer)

    async def read_message(self, peer):
        size = struct.unpack(">l", await peer.reader.read(4))
        message = await peer.reader.read(size)
        return message

