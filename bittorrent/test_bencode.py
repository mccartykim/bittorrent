#! /usr/bin/python3

import unittest
import bencode
from hypothesis import given
from hypothesis.strategies import binary, integers, lists, dictionaries


class TestBencodeMethods(unittest.TestCase):

    @given(binary())
    def test_invert_string(self, s):
        p = bencode.Parser()
        self.assertEqual(p.parse(bencode.encode(s)), s)

    @given(integers())
    def test_invert_integer(self, n):
        p = bencode.Parser()
        self.assertEqual(n, p.parse(bencode.encode(n)))

    @given(lists(binary(), max_size=99))
    def test_invert_lists(self, l):
        p = bencode.Parser()
        print(l)
        self.assertEqual(p.parse(bencode.encode(l)), l)

    def test_encode(self):
        # int
        self.assertEqual(b"i32e", bencode.encode(32))
        self.assertEqual(b"i-32e", bencode.encode(-32))
        # dict
        self.assertEqual(b"d3:foo3:bare", bencode.encode({"foo": "bar"}))
        # list
        self.assertEqual(b"l3:foo3:poei2ee", bencode.encode(["foo", "poe", 2]))
        # strings
        self.assertEqual(b"5:hello", bencode.encode("hello"))
        self.assertEqual(b"5:hello", bencode.encode(b"hello"))
        self.assertEqual(b"5:hello", bencode.encode("hello".encode("utf-8")))
        # empty values
        self.assertEqual(b"le", bencode.encode([]))
        self.assertEqual(b"de", bencode.encode({}))
        # NOTE: consider testing nesting in some way?

    def test_parse(self):
        p = bencode.Parser()
        self.assertEqual(p.parse(b"i32e"), 32)
        self.assertEqual(p.parse(b"i-32e"), -32)
        self.assertEqual(p.parse(b"de"), {})
        self.assertEqual(p.parse(b"d3:foo3:bare"), {b"foo": b"bar"})
        # FIGURE OUT HOW TO TEST INFOHASH


if __name__ == "__main__":
    unittest.main()
