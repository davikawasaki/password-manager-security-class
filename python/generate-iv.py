#!/usr/bin/python

import os
import sys

# Get intermediate key
key = open('keys/raw/' + sys.argv[1] + '.key', 'rb').read()

# Write iv depending on key block size
iv = os.urandom(len(key)/2)
ff = open('data/crypto/' + sys.argv[2] + '_' + str(len(key)/2) + '.txt', 'w')
ff.write(iv)
ff.close()