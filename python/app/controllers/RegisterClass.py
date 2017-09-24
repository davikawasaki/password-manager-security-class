import htmlPy, json
import os, sys
from Crypto.Protocol import KDF
from Crypto.Cipher import AES
import hashlib
import CommonClass as CC
import ListDataClass as LDC

KEY_LENGTH = 32

class Register(htmlPy.Object):

    def __init__(self, app):
        super(Register, self).__init__()
        self.app = app
        self.common = CC.Common(self.app)
        self.listData = LDC.ListData(self.app)

    @htmlPy.Slot()
    def loadRegUser(self):
        self.app.template = ("register.html", {})

    @htmlPy.Slot(str, result=str)
    def regUser(self, json_data="[]"):
        data = json.loads(json_data)
        print data
        if(not data['username'] or not data['password']):
            self.app.template = ("register.html", {"error": "User and/or password can't be empty!"})
        elif self.checkUserExistence('password', data['username']):
            self.app.template = ("register.html", {"error": "Username already registered!"})
        else:
            # ENCRYPT INTERMEDIARY KEY WITH KDF PASSWORD
            # Generate salt for KDF encryption and iv for key encryption
            salt = self.common.genSalt('password', data['username'])
            iv = self.common.genIV('password', data['username'])

            # Generate intermediary key
            key = self.common.genRandom()
            key_padded = self.common.pad(key, len(key))

            # Hash password and encript intermediary key
            self.common.genHash(data['password'], 'password', data['username'])
            self.common.encKey(data['password'], key_padded, salt, iv, 'password', data['username'])

            # ENCRYPT INTERMEDIARY KEY WITH KDF RECOVERY CODE
            # Generate salt for KDF encryption and iv for key encryption
            salt = self.common.genSalt('reccode', data['username'])
            iv = self.common.genIV('reccode', data['username'])

            # Hash recovery code and encript intermediary key
            reccode = self.common.genRecCode()
            self.common.genHash(reccode, 'reccode', data['username'])
            self.common.encKey(reccode, key_padded, salt, iv, 'reccode', data['username'])

            # Generate info encryption iv
            ivD = self.common.genIV('data', data['username'])
            
            self.listData.listInfoAfterRegister(data, reccode)

    def checkUserExistence(self, fileType, user):
        try:
            hf = open(os.path.dirname(__file__) + '/../data/security/hash_' + fileType + '_' + user + '.txt', 'rb').read()
            if(hf):
                return True
            else:
                return False
        except IOError:
            return False   