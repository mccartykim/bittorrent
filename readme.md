# Everybody's Writing Bit Torrent #
so why not me?

good question, actually.

So far I have the Bencoder parser/encoder running.  I'm pretty proud of it, despite its simplicity and lack of tolerance for malformed strings.  I will probably try to work in some kind of ruggedness in the face of spicy/naughty strings, but for now, I'm just thrilled it works with good input.

Update: Now it handles bytestrings a bit more rationally, and is able to request a get request from a server.  Still an EXTREME WIP.  But I'm pleasantly surprised with how much I can get done with simple bencoding and requests.
