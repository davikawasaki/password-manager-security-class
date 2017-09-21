#!/usr/bin/python

import os
import sys

# AES-256 bit key = 32 bytes
keylength = int(sys.argv[1])

# Write intermediate key
key = os.urandom(keylength)
ff = open('keys/raw/aes' + sys.argv[1] + '.key', 'w')
ff.write(key)
ff.close()

# Write iv depending on key block size
iv = os.urandom(len(key)/2)
ff = open('data/crypto/iv_data_' + str(len(key)/2) + '.txt', 'w')
ff.write(iv)
ff.close()