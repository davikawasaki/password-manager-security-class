#!/usr/bin/python

from Crypto.Protocol import KDF
from Crypto.Cipher import AES
from argparse import ArgumentParser
import base64, sys, os

class DecryptKeys:

    def __init__( self, password, salt ):
        self.password = password
        self.salt = salt

    def decriptInterKey( self, enc ):

        # Generate password derived key to encript AES-32 intermediary key
        password_key = KDF.PBKDF2(self.password, self.salt, 32, 1000, None)
        
        # Start the initializing vector
        iv = open('data/crypto/iv_password_16.txt', 'rb').read()
        # Create the cipher object and process the input stream
        cipher = AES.AESCipher(password_key, AES.MODE_CBC, iv)
        return self.unpad(cipher.decrypt(enc[len(password_key)/2:]))

    # Remove padding from clear text
    def unpad ( self, s ):
        return s[0:-ord(s[-1])]

salt = open('data/crypto/salt_password_32.txt', 'rb').read()
cipher = DecryptKeys(sys.argv[1], salt)

key_ciphered = open('keys/aes-enc-32.key', 'rb').read()
key = cipher.decriptInterKey(key_ciphered)

print 'Decoded intermediary key: ' + key.encode('base-64')
print 'Non-touched intermediary key: ' + open('keys/raw/aes32.key', 'rb').read().encode('base-64')