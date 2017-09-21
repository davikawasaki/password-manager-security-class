#!/usr/bin/python

from Crypto.Cipher import AES
from argparse import ArgumentParser
import base64, sys, os

class DecryptData:

    def __init__( self, key, msg ):
        self.key = key
        self.enc = enc
    
    def decrypt( self ):

        key_len = len(self.key)
        enc = self.enc
        # Start the initializing vector
        iv = enc[:key_len/2]
        # Create the cipher object and process the input stream
        cipher = AES.AESCipher(self.key, AES.MODE_CBC, iv)
        # print self.unpad(cipher.decrypt(enc[key_len/2:])).encode('base-64')
        return self.unpad(cipher.decrypt(enc[key_len/2:]))

    # Remove padding from clear text
    def unpad ( self, s ):
        return s[0:-ord(s[-1])]

key = open('keys/raw/aes32.key', 'rb').read()
enc = open('data/service-enc-001.txt', 'rb').read()
# Instantiate decryptData, returning a cipher with a key attr
cipher = DecryptData(key, enc)
decryptedData = cipher.decrypt()

ff = open('data/raw/service-001.txt', 'w')
ff.write(decryptedData)
ff.close()

# print decryptedData.encode('base-64')