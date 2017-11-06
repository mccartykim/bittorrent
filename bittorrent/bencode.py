#! /usr/bin/python3
"""bencode for Bittorrent
By Kimberly McCarty
It's for fun, okay?
"""
from collections import OrderedDict
import string
import re
import hashlib
import logging

# FIXME: Ensure the entire encoder works with bytes!



def encode(e):
    if type(e) == list:
        return encode_list(e)
    elif type(e) == dict:
        return encode_dict(e)
    elif type(e) == int:
        return encode_integer(e)
    elif (type(e) == str) or (type(e) == bytes):
        return encode_string(e)
    else:
        raise(ValueError("Invalid type, must be str, int, list, or dict"))


class Parser(object):
    def __init__(self):
        self.cursor = 0
        self.s = b""

    # return character at current position
    def _char(self):
        return chr(self.s[self.cursor])

    def parse(self, s):
        # Assume a full statement is a well-formed entire Bencoded statement
        # This statement is not to be called recursively,
        # it just manages the initial call and sets cursor/s to valid values
        self.s = s
        if type(self.s) != bytes:
            self.s = self.s.encode()
        self.cursor = 0
        result = self.b()
        return result

    def b(self):
        char = self._char()
        if char == "l":
            return self.l()
        elif char == "d":
            return self.d()
        elif char == "i":
            return self.i()
        elif char in string.digits:
            return self.string()
        else:
            logging.info("B found nonetype")
            print("B found nonetype")
            return None


    #broke grammar rule nomenclature to prevent confusion with self.s, our string buffer
    def string(self):
        # decoding ignores "illegal" characters, because only digits and colon will be of concern to us, and if those aren't there, this isn't a string
        len_raw = re.search(r"^(\d*):", self.s[self.cursor::].decode("utf-8", "ignore")).group(1)
        len_int = int(len_raw)
        # get the string from length of the integer descriptor, plus one for the ':'
        start = self.cursor + len(len_raw) + 1
        end = start + len_int
        str_ = self.s[start:end]
        #move cursor past this stuff for the next thing to parse
        self.cursor = end
        assert(len(str_) == len_int)
        assert(type(str_) == bytes)
        return str_

    def i(self):
        assert(self._char() == 'i')
        raw, i_raw = re.search("^(i(-?\d*)e)", self.s[self.cursor::].decode("utf-8", "ignore")).groups()
        i_ = int(i_raw)
        len_ = len(raw)
        #move past what we've parsed to the next thing
        self.cursor += len_
        return i_


    # It can't be this simple!  Recursion is wild! This is supposed to be hard!  I'm screwing up in a way I haven't recognised!
    def l(self):
        assert(self._char() == "l")
        self.cursor += 1
        result = []
        while self._char() != "e":
            result.append(self.b())
        self.cursor += 1
        return result


    def d(self):
    
        assert(self._char() == "d")
        self.cursor += 1
        result = {}
        while self._char() != "e":
            key = self.string()
            result[key] = self.b()
        self.cursor += 1
        return result 

    def get_info_hash(self, path=None, dict_=None):
        assert(path or dict_)
        if path:
            with open(path) as f:
                metainfo = self.parse(f.read)
        elif dict_:
            metainfo = dict_
        info = metainfo[b'info']
        info_ben = encode(info)
        #print(info_ben)
        m = hashlib.sha1()
        m.update(info_ben)
        return m.digest()
        


#Helper functions for encode()
def encode_string(s):
    l = len(s)
    if type(s) == bytes:
        return bytes(str(l)+":", "utf-8") + s
    # Assume if there's no bytestring, our string can be represented in UTF-8
    return "{}:{}".format(l, s).encode("utf-8")


def encode_integer(i):
    return "i{}e".format(str(i)).encode("utf-8")


def encode_list(l):
    encoded = bytearray(b'l')
    for e in l:
        encoded.extend(encode(e))
    encoded.append(ord('e'))
    return bytes(encoded)


def encode_dict(d):
    encoded = bytearray(b'd')
    # TODO consider accounting for weird raw bytestring behavior...
    od = OrderedDict(sorted(d.items()))
    for key, value in od.items():
        assert(type(key) == str or type(key) == bytes)
        encoded.extend(encode(key))
        encoded.extend(encode(value))
    encoded.append(ord("e"))
    return bytes(encoded)

# the code below was used to test this with a sample torrent file
# if __name__ == "__main__":
#     with open("sample.torrent", "rb") as f:
#         p = Parser()
#         print(p.parse(f.read()))
