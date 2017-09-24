import htmlPy, json, datetime, time
import os, sys, re, fnmatch
from Crypto.Protocol import KDF
from Crypto.Cipher import AES
import hashlib

KEY_LENGTH = 32

class Common(htmlPy.Object):

    def __init__(self, app):
        super(Common, self).__init__()
        self.app = app

    def checkAuth(self, fileType, pw, user):
        if(not user or not pw):
            return False
        else: 
            try:
                hf = open(os.path.dirname(__file__) + '/../data/security/hash_' + fileType + '_' + user + '.txt', 'r').read()
                hash = hashlib.sha256(pw).hexdigest()
                if(hash == hf):
                    return True
                else:
                    return False
            except IOError:
                return False

    def pad(self, s, bs):
        return s + (bs - len(s) % bs) * chr(bs - len(s) % bs)

    def unpad(self, s):
        return s[0:-ord(s[-1])]

    def ts2str(self, ts):
        ts = float(ts)
        return datetime.datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")

    def genTimestamp(self):
        return time.mktime(datetime.datetime.now().timetuple())

    def genRandom(self):
        return os.urandom(KEY_LENGTH)

    def genSalt(self, fileType, user):
        # Randomly generate a fileType salt
        sf = open(os.path.dirname(__file__) + '/../data/security/salt_' + fileType + '_' + str(KEY_LENGTH) + '_' + user + '.txt', 'w')
        salt = os.urandom(KEY_LENGTH)
        sf.write(salt)
        sf.close()
        return salt

    def genIV(self, fileType, user):
        # Randomly generate a fileType iv
        ivf = open(os.path.dirname(__file__) + '/../data/security/iv_' + fileType + '_' + str(KEY_LENGTH/2) + '_' + user + '.txt', 'w')
        iv = os.urandom(KEY_LENGTH/2)
        ivf.write(iv)
        ivf.close()
        return iv

    def decKey(self, fileType, pw, user):
        # Read password salt and iv
        iv = open(os.path.dirname(__file__) + '/../data/security/iv_'  + fileType + '_' + str(KEY_LENGTH/2) + '_' + user + '.txt', 'r').read()
        salt = open(os.path.dirname(__file__) + '/../data/security/salt_'  + fileType + '_' + str(KEY_LENGTH) + '_' + user + '.txt', 'r').read()

        # Read encrypted intermediary key
        enc = open(os.path.dirname(__file__) + '/../data/security/aes_' + fileType + '_enc_' + str(KEY_LENGTH) + '_' + user + '.key' , 'r').read()

        # Generate KDF secret key
        pk = KDF.PBKDF2(pw, salt, KEY_LENGTH, 1000, None)

        # Create the cipher object and decrypt intermediary key with KDF secret key
        cipher = AES.AESCipher(pk, AES.MODE_CBC, iv)
        return self.unpad(cipher.decrypt(enc[len(pk)/2:]))

    def encKey(self, pw, key, salt, iv, fileType, user):
        # Generate KDF secret key
        pk = KDF.PBKDF2(pw, salt, KEY_LENGTH, 1000, None)

        # Create the cipher object and encrypt intermediary key with KDF secret key
        cipher = AES.AESCipher(pk, AES.MODE_CBC, iv)

        encKey = iv + cipher.encrypt(key)
        self.storeEncKey(encKey, fileType, user)

    def storeEncKey(self, encKey, fileType, user):
        kf = open(os.path.dirname(__file__) + '/../data/security/aes_' + fileType + '_enc_' + str(KEY_LENGTH) + '_' + user + '.key', 'w')
        kf.write(encKey)
        kf.close()

    def genRecCode(self):
        return os.urandom(KEY_LENGTH/4).encode('base-64')

    def genHash(self, pw, fileType, user):
        hf = open(os.path.dirname(__file__) + '/../data/security/hash_' + fileType + '_' + user + '.txt', 'w')
        hf.write(hashlib.sha256(pw).hexdigest())
        hf.close()