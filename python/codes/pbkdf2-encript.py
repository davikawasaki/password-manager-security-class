#!/usr/bin/python

from Crypto.Protocol import KDF
from Crypto.Cipher import AES
from argparse import ArgumentParser
import base64, sys, os

class EncryptKeys:

    def __init__( self, password, salt ):
        self.password = password
        self.salt = salt

    def encriptInterKey( self, key ):

        # Generate password derived key to encript AES-32 intermediary key
        password_key = KDF.PBKDF2(self.password, self.salt, len(key), 1000, None)
        
        # Insert padding to intermediary key
        key_padded = self.pad(key, len(password_key))

        # Get password initializing vector
        iv = open('data/crypto/iv_password_16.txt', 'rb').read()
        # Create the cipher object and process the input stream
        cipher = AES.AESCipher(password_key, AES.MODE_CBC, iv)

        return (iv + cipher.encrypt(key_padded))

    # Input padding inside clear text
    def pad ( self, s, bs ):
        return s + (bs - len(s) % bs) * chr(bs - len(s) % bs)

salt = open('data/crypto/salt_password_32.txt', 'rb').read()
cipher = EncryptKeys(sys.argv[1], salt)

key = open('keys/raw/aes32.key', 'rb').read()
key_ciphered = cipher.encriptInterKey(key)

ff = open('keys/aes-enc-32.key', 'w')
ff.write(key_ciphered)
ff.close()

print key_ciphered.encode('base-64')