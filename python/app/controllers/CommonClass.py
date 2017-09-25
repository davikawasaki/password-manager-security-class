import htmlPy
import datetime
import time
import os
from Crypto.Protocol import KDF
from Crypto.Cipher import AES
import hashlib

KEY_LENGTH = 32

class Common(htmlPy.Object):

    """ Common service class with cryptography methods.

    The class Common can be used to implement any common methods between controllers.

    """

    def __init__(self, app):
        super(Common, self).__init__()
        self.app = app

    def checkAuth(self, fileType, pw, user):
        if(not user or not pw):
            return False
        else: 
            try:
                path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/data/security/hash_' + fileType + '_' + user + '.txt'
                hf = open(path, 'r').read()
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
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/data/security/salt_' + fileType + '_' + str(KEY_LENGTH) + '_' + user + '.txt'
        sf = open(path, 'w')
        salt = os.urandom(KEY_LENGTH)
        sf.write(salt)
        sf.close()
        return salt

    def genIV(self, fileType, user):
        # Randomly generate a fileType iv
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/data/security/iv_' + fileType + '_' + str(KEY_LENGTH/2) + '_' + user + '.txt'
        ivf = open(path, 'w')
        iv = os.urandom(KEY_LENGTH/2)
        ivf.write(iv)
        ivf.close()
        return iv

    def decKey(self, fileType, pw, user):
        # Read password salt and iv
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/data/security/iv_'  + fileType + '_' + str(KEY_LENGTH/2) + '_' + user + '.txt'
        iv = open(path, 'r').read()
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/data/security/salt_'  + fileType + '_' + str(KEY_LENGTH) + '_' + user + '.txt'
        salt = open(path, 'r').read()

        # Read encrypted intermediary key
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/data/security/aes_' + fileType + '_enc_' + str(KEY_LENGTH) + '_' + user + '.key'
        enc = open(path, 'r').read()

        # Generate KDF secret key
        pk = KDF.PBKDF2(pw, salt, KEY_LENGTH, 1000, None)

        # Create the cipher object and decrypt intermediary key with KDF secret key
        cipher = AES.AESCipher(pk, AES.MODE_CBC, iv)
        key = self.unpad(cipher.decrypt(enc[len(pk)/2:]))
        # print 'deckey ' + fileType + ': ' + key.encode('base-64')
        return key

    def encKey(self, pw, key, salt, iv, fileType, user):
        # Generate KDF secret key
        pk = KDF.PBKDF2(pw, salt, KEY_LENGTH, 1000, None)

        # Pad intermediary key with pk length
        key_padded = self.pad(key, len(pk))

        # Create the cipher object and encrypt intermediary key with KDF secret key
        cipher = AES.AESCipher(pk, AES.MODE_CBC, iv)

        encKey = iv + cipher.encrypt(key_padded)
        # print 'enckey ' + fileType + ': ' + encKey.encode('base-64')
        self.storeEncKey(encKey, fileType, user)

        key = None
        key_padded = None

    def storeEncKey(self, encKey, fileType, user):
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/data/security/aes_' + fileType + '_enc_' + str(KEY_LENGTH) + '_' + user + '.key'
        kf = open(path, 'w')
        kf.write(encKey)
        kf.close()

    def genRecCode(self):
        return os.urandom(KEY_LENGTH/4)

    def genHash(self, pw, fileType, user):
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/data/security/hash_' + fileType + '_' + user + '.txt'
        hf = open(path, 'w')
        hf.write(hashlib.sha256(pw).hexdigest())
        hf.close()