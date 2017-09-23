import htmlPy, json
import os, sys, re, fnmatch
from Crypto.Protocol import KDF
from Crypto.Cipher import AES
import hashlib

KEY_LENGTH = 32

class ListData(htmlPy.Object):

    def __init__(self, app):
        super(ListData, self).__init__()
        self.app = app

    @htmlPy.Slot(str, result=str)
    def logUser(self, data):
        if self.checkAuth('password', data.password, data.username):
            self.listInfo(data)
        else:
            self.app.template = ("index.html", {"error": "User and/or password invalid!"})

    @htmlPy.Slot(str, result=str)
    def listInfo(self, data):
        # Get decrypted intermediary key
        key = self.decryptKey('password', data.password, data.username)
        # Open iv to encrypt data info
        iv = open('../data/security/iv_data_' + str(KEY_LENGTH/2) + '_' + data.username + '.txt').read()
        
        # Create the cipher object and process the input stream
        cipher = AES.AESCipher(key, AES.MODE_CBC, iv)

        # Decrypt info files
        userData = self.decryptInfoFiles(cipher, len(key), self.listUserData(data.username))
        key = None
        
        return userData

    @htmlPy.Slot(str, result=str)
    def removeInfo(self, data):
        if self.checkAuth('password', data.password, data.username):
            # Get decrypted intermediary key
            key = self.decryptKey('password', data.password, data.username)
            # Remove file from respective info
            os.remove('../data/info/' + data.infoName + '_enc_' + data.username + '_' + data.timestamp + '.txt')

            return True
        else:
            return 'Senha incorreta!'

    def checkAuth(self, fileType, pw, user):
        hf = open('../data/security/hash_' + fileType + '_' + user + '.txt', 'rb').read()
        hash = hashlib.sha256(pw).hexdigest()
        if(hash == hf):
            return True
        else:
            return False

    def decryptKey(self, fileType, pw, user):
        # Read password salt and iv
        iv = open('../data/security/iv_'  + fileType + '_' + str(KEY_LENGTH/2) + '_' + user + '.txt', 'rb').read()
        salt = open('../data/security/salt_'  + fileType + '_' + str(KEY_LENGTH) + '_' + user + '.txt', 'rb').read()

        # Read encrypted intermediary key
        enc = open('../data/security/aes_' + fileType + '_enc_' + str(KEY_LENGTH) + '_' + user + '.key' , 'rb').read()

        # Generate KDF secret key
        pk = KDF.PBKDF2(pw, salt, KEY_LENGTH, 1000, None)

        # Create the cipher object and decrypt intermediary key with KDF secret key
        cipher = AES.AESCipher(pk, AES.MODE_CBC, iv)
        return self.unpad(cipher.decrypt(enc[len(pk)/2:]))

    def listUserData(self, user):
        userData = []
        for file in os.listdir('data/info'):
            if fnmatch.fnmatch(file, '*_' + user + '_*.txt'):
                userData.append('../data/info/' + file)
        return userData

    def decryptInfoFiles(self, cipher, keyLen, userData):
        userDataDec = []
        for file in userData:
            # Get service name
            m = re.match(r'../data/info/(.*)_enc_(.*?)_(.*?).txt', file, re.M|re.I)
            # Decrypt service pw
            enc = open(file , 'rb').read()
            pw = self.unpad(cipher.decrypt(enc[keyLen/2:]))

            class data: name = m.group(1); y = pw
            userDataDec.append(data)
        return userDataDec

    def pad(self, s, bs):
        return s + (bs - len(s) % bs) * chr(bs - len(s) % bs)

    def unpad (self, s):
        return s[0:-ord(s[-1])]
