import htmlPy, json, datetime
import os, sys, re, fnmatch
from Crypto.Protocol import KDF
from Crypto.Cipher import AES
import hashlib
import CommonClass as CC

KEY_LENGTH = 32

class ListData(htmlPy.Object):

    def __init__(self, app):
        super(ListData, self).__init__()
        self.app = app
        self.common = CC.Common(self.app)

    @htmlPy.Slot(str, result=str)
    def listInfo(self, data, modalError):
        # Get decrypted intermediary key
        key = self.common.decKey('password', data['password'], data['username'])
        # Open iv to encrypt data info
        iv = open(os.path.dirname(__file__) + '/../data/security/iv_data_' + str(KEY_LENGTH/2) + '_' + data['username'] + '.txt').read()

        # Decrypt info files
        userData = self.decryptInfoFiles(key, iv, len(key), self.listUserData(data['username']))
        key = None

        self.app.template = ("passwords.html", {"userData": userData, "username": data['username'], "modalError": modalError})

    def listInfoAfterRegister(self, data, reccode):
        self.app.template = ("passwords.html", {"reccode": reccode, "username": data['username']})

    def listUserData(self, user):
        userData = []
        for file in os.listdir(os.path.dirname(__file__) + '/../data/info'):
            if fnmatch.fnmatch(file, '*_' + user + '_*.txt'):
                userData.append('/../data/info/' + file)
        return userData

    def decryptInfoFiles(self, key, iv, keyLen, userData):
        userDataDec = []
        for file in userData:
            # Get service name (data_enc_username_timestamp.txt)
            m = re.match(r'/../data/info/data_enc_(.*?)_(.*?).txt', file, re.M|re.I)
            # Decrypt service pw
            enc = open(os.path.dirname(__file__) + file , 'r').read()
            # Create the cipher object and process the input stream
            cipher = AES.AESCipher(key, AES.MODE_CBC, iv)
            # [ Service name / Login / Pw ]
            loginPw = self.common.unpad(cipher.decrypt(enc[keyLen/2:])).splitlines()

            class data: name = loginPw[0]; login = loginPw[1]; password = loginPw[2]; timestamp = m.group(2)

            userDataDec.append(data)
        return userDataDec