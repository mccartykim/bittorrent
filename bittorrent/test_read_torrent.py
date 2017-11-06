import read_torrent
import unittest
import struct
from ipaddress import IPv4Address


class TestReadTorrent(unittest.Testcase):

    def test_unpack_peers(self, path):
        peer_pack = bytes(chr(192) + chr(168) + chr(1) + chr(1), "ascii")
        peer_pack += struct.pack("!H", 6999)
        first_peer = read_torrent.unpack_peers(peer_pack)[0]
        self.assertEqual(first_peer[0], IPv4Address("192.168.1.1"))
        self.assertEqual(first_peer[1], 6999)
