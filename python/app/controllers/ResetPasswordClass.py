import htmlPy, json
import os, sys
from Crypto.Protocol import KDF
from Crypto.Cipher import AES
import hashlib
import CommonClass as CC
import ListDataClass as LDC

KEY_LENGTH = 32

class ResetPassword(htmlPy.Object):

    def __init__(self, app):
        super(ResetPassword, self).__init__()
        self.app = app
        self.common = CC.Common(self.app)
        self.listData = LDC.ListData(self.app)

    @htmlPy.Slot()
    def loadResetPw(self):
        print '[LOG] Loading reset pw page...'
        self.app.template = ("reset.html", {})

    @htmlPy.Slot(str, result=str)
    def resetPw(self, json_data="[]"):
        print '[LOG] Reseting pw process...'
        data = json.loads(json_data)        
        if(not data['username'] or not data['password'] or not data['reccode']):
            self.app.template = ("reset.html", {"error": "User and/or password/recovery code can't be empty!"})
        # Decode reccode before hashing
        elif self.common.checkAuth('reccode', data['reccode'].decode('base-64'), data['username']):
            # Check user and reccode
            # Get decrypted intermediary key from reccode
            key = self.common.decKey('reccode', data['reccode'], data['username'])
            
            # Encrypt intermediary secret pw with new master password
            # Generate salt for KDF encryption and iv for key encryption
            salt = self.common.genSalt('password', data['username'])
            iv = self.common.genIV('password', data['username'])

            # Hash new master password and encript intermediary key
            # Overwrite encrypted intermediary secret pw
            self.common.genHash(data['password'], 'password', data['username'])
            self.common.encKey(data['password'], key, salt, iv, 'password', data['username'])

            # Generate salt for KDF encryption and iv for key encryption
            salt = self.common.genSalt('reccode', data['username'])
            iv = self.common.genIV('reccode', data['username'])

            # Generate new reccode
            # Encrypt intermediary secret pw with new reccode
            # Hash recovery code and encript intermediary key
            # Overwrite encrypted intermediary secret pw
            reccode = self.common.genRecCode()
            self.common.genHash(reccode, 'reccode', data['username'])
            self.common.encKey(reccode, key, salt, iv, 'reccode', data['username'])
            
            key = None
            
            # Load passwords list with new reccode
            self.listData.listInfoAfterRegister(data, reccode.encode('base-64'))
        else:
            self.app.template = ("reset.html", {"error": "User and/or recovery code invalid!"})