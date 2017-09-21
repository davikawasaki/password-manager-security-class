#!/usr/bin/python

from Crypto.Cipher import AES
from argparse import ArgumentParser
import base64, sys, os

class EncryptData:

    def __init__( self, key, msg ):
        self.key = key
        self.msg = msg
    
    def encrypt( self ):

        key_len = len(self.key)
        msg = self.pad(self.msg, key_len)

        # Start the initializing vector
        iv = os.urandom(key_len/2)
        # Create the cipher object and process the input stream
        cipher = AES.AESCipher(key, AES.MODE_CBC, iv)

        return (iv + cipher.encrypt(msg))

    # Input padding inside clear text
    def pad ( self, s, bs ):
        return s + (bs - len(s) % bs) * chr(bs - len(s) % bs)

key = open('keys/raw/aes32.key', 'rb').read()
password = sys.argv[1]
# Instantiate encryptData, returning a cipher with a key attr
cipher = EncryptData(key, password)
encryptedData = cipher.encrypt()

ff = open('data/service-enc-001.txt', 'w')
ff.write(encryptedData)
ff.close()

print encryptedData.encode('base-64')