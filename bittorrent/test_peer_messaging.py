#! /usr/bin/python3

import unittest
import peer_messaging


class TestPeer(unittest.Testcase):
    def test_peer_object(self):
        ptuple = ("192.168.1.1", 6999)
        metainfo = {b'pieces': [b"a" * 20] * 120}
        peer = peer_messaging(ptuple, metainfo)
        self.assertEqual(peer.address, "192.168.1.1")
        self.assertEqual(peer.port, 6999)


class TestPeerMessenger(unittest.Testcase):
    def test_peer_messenger(self):
        return None
