import htmlPy, json
import os, sys
from Crypto.Protocol import KDF
from Crypto.Cipher import AES
import hashlib

KEY_LENGTH = 32

class Register(htmlPy.Object):

    def __init__(self, app):
        super(Register, self).__init__()
        self.app = app

    @htmlPy.Slot(str, result=str)
    def regUser(self, json_data="[]"):
        data = json.loads(json_data)
    
        # ENCRYPT INTERMEDIARY KEY WITH KDF PASSWORD
        # Generate salt for KDF encryption and iv for key encryption
        salt = self.genSalt('password', data['username'])
        iv = self.genIV('password', data['username'])

        # Generate intermediary key
        key = self.genRandom()
        key_padded = self.pad(key, len(key))

        # Hash password and encript intermediary key
        self.genHash(data['password'], 'password', data['username'])
        self.encIntKey(data['password'], key_padded, salt, iv, 'password', data['username'])

        # ENCRYPT INTERMEDIARY KEY WITH KDF RECOVERY CODE
        # Generate salt for KDF encryption and iv for key encryption
        salt = self.genSalt('reccode', data['username'])
        iv = self.genIV('reccode', data['username'])

        # Hash recovery code and encript intermediary key
        reccode = self.genRecCode()
        self.genHash(reccode, 'reccode', data['username'])
        self.encIntKey(reccode, key_padded, salt, iv, 'reccode', data['username'])

        # Generate info encryption iv
        ivD = self.genIV('data', data['username'])
        self.app.template = ("test.html", {})

    def genRandom(self):
        return os.urandom(KEY_LENGTH)

    def pad(self, s, bs):
        return s + (bs - len(s) % bs) * chr(bs - len(s) % bs)

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

    def encIntKey(self, pw, key, salt, iv, fileType, user):
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