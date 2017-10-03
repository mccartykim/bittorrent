"""bencode for Bittorrent
By Kimberly McCarty
It's for fun, okay?
"""
from collections import OrderedDict
import string
import re



def encode(e):
    if type(e) == list:
        return encode_list(e)
    elif type(e) == dict:
        return encode_dict(e)
    elif type(e) == int:
        return encode_integer(e)
    elif type(e) == str:
        return encode_string(e)
    else:
        raise(ValueError("Invalid type, must be str, int, list, or dict"))

class Parser(object):
    def __init__(self):
        self.cursor = 0
        self.s = ""


    def parse(self, s):
        # Assume a full statement is a well-formed entire Bencoded statement
        # This statement is not to be called recursively, it just manages the initial call and sets cursor/s to valid values
        self.s = s
        self.cursor = 0
        result = self.b()
        return result

    def b(self):
        char = self.s[self.cursor]
        if char == "l":
            return self.l()
        elif char == "d":
            return self.d()
        elif char == "i":
            return self.i()
        elif char in string.digits:
            return self.string()


    #broke grammar rule nomenclature to prevent confusion with self.s, our string buffer
    def string(self):
        len_raw = re.search(r"^(\d*):", self.s[self.cursor::]).group(1)
        len_int = int(len_raw)
        # get the string from length of the integer descriptor, plus one for the ':'
        start = self.cursor + len(len_raw) + 1
        end = start + len_int
        str_ = self.s[start:end]
        #move cursor past this stuff for the next thing to parse
        self.cursor = end
        assert(len(str_) == len_int)
        return str_

    def i(self):
        assert(self.s[self.cursor] == 'i')
        raw, i_raw = re.search("^(i(-?\d*)e)", self.s[self.cursor::]).groups()
        i_ = int(i_raw)
        len_ = len(raw)
        #move past what we've parsed to the next thing
        self.cursor += len_
        return i_


    # It can't be this simple!  Recursion is wild! This is supposed to be hard!  I'm screwing up in a way I haven't recognised!
    def l(self):
        assert(self.s[self.cursor] == "l")
        self.cursor += 1
        result = []
        while self.s[self.cursor] != "e":
            result += b
        self.cursor += 1
        return result


    def d(self):
        assert(self.s[self.cursor] == "d")
        self.cursor += 1
        result = {}
        while self.s[self.cursor] != "e":
            key = self.string()
            result[key] == self.b()
        self.cursor += 1
        return result 


#Helper functions for encode()
def encode_string(s):
    l = len(s)
    return "{}:{}".format(l, s)


def encode_integer(i):
    return "i{}e".format(str(i))


def encode_list(l):
    encoded = []
    for e in l:
        encoded.append(encode(e))
    return "l{}e".format("".join(encoded))


def encode_dict(d):
    encoded = []
    # TODO consider accounting for weird raw bytestring behavior...
    od = OrderedDict(sorted(d.items()))
    for key, value in od.items():
        assert(type(key) == str)
        encoded.append(encode(key))
        encoded.append(encode(value))
    return "d{}e".format("".join(encoded))
