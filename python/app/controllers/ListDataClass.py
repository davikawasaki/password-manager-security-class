import htmlPy
import json
import os
import re
import fnmatch
from Crypto.Cipher import AES
import CommonClass as CC

KEY_LENGTH = 32

class ListData(htmlPy.Object):

    def __init__(self, app):
        super(ListData, self).__init__()
        self.app = app
        self.common = CC.Common(self.app)

    @htmlPy.Slot(str, result=str)
    def listInfo(self, data, modalError):
        print '[LOG] Listing user service info...'
        # Get decrypted intermediary key
        key = self.common.decKey('password', data['password'], data['username'])
        # Open iv to encrypt data info
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/data/security/iv_data_' + str(KEY_LENGTH/2) + '_' + data['username'] + '.txt'
        iv = open(path).read()

        # Decrypt info files
        userData = self.decryptInfoFiles(key, iv, len(key), self.listUserData(data['username']))

        self.app.template = ("passwords.html", {"userData": userData, "username": data['username'], "modalError": modalError})
        key = None

    def listInfoAfterRegister(self, data, reccode):
        self.app.template = ("passwords.html", {"reccode": reccode, "username": data['username']})

    def listUserData(self, user):
        userData = []
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/data/info/'
        for file in os.listdir(path):
            if fnmatch.fnmatch(file, '*_' + user + '_*.txt'):
                userData.append('/data/info/' + file)
        return userData

    def decryptInfoFiles(self, key, iv, keyLen, userData):
        userDataDec = []
        for file in userData:
            # Get service name (data_enc_username_timestamp.txt)
            path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + file
            m = re.match(r'(.*?)/data/info/data_enc_(.*?)_(.*?).txt', path, re.M|re.I)
            # Decrypt service pw
            enc = open(path , 'r').read()
            # Create the cipher object and process the input stream
            cipher = AES.AESCipher(key, AES.MODE_CBC, iv)
            # [ Service name / Login / Pw ]
            loginPw = self.common.unpad(cipher.decrypt(enc[keyLen/2:])).splitlines()

            class data: name = loginPw[0]; login = loginPw[1]; password = loginPw[2]; timestamp = m.group(3)

            userDataDec.append(data)
        return userDataDec