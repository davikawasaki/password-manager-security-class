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
        print '[LOG] Loading new user registration page...'
        self.app.template = ("register.html", {})

    @htmlPy.Slot(str, result=str)
    def regUser(self, json_data="[]"):
        print '[LOG] Registering new user...'
        data = json.loads(json_data)
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
            print key.encode('base-64')

            # Hash password and encript intermediary key
            self.common.genHash(data['password'], 'password', data['username'])
            self.common.encKey(data['password'], key, salt, iv, 'password', data['username'])

            # ENCRYPT INTERMEDIARY KEY WITH KDF RECOVERY CODE
            # Generate salt for KDF encryption and iv for key encryption
            salt = self.common.genSalt('reccode', data['username'])
            iv = self.common.genIV('reccode', data['username'])

            # Hash recovery code and encript intermediary key
            reccode = self.common.genRecCode()
            self.common.genHash(reccode, 'reccode', data['username'])
            self.common.encKey(reccode, key, salt, iv, 'reccode', data['username'])

            # Generate info encryption iv
            ivD = self.common.genIV('data', data['username'])

            key = None
            
            self.listData.listInfoAfterRegister(data, reccode.encode('base-64'))

    def checkUserExistence(self, fileType, user):
        try:
            path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/data/security/hash_' + fileType + '_' + user + '.txt'
            hf = open(path, 'rb').read()
            if(hf):
                return True
            else:
                return False
        except IOError:
            return False   