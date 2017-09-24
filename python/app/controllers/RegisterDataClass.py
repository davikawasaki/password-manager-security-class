import htmlPy, json
import os, sys, time, datetime
from Crypto.Protocol import KDF
from Crypto.Cipher import AES
import hashlib
import ListDataClass as LDC
import CommonClass as CC

KEY_LENGTH = 32

class RegisterData(htmlPy.Object):

    def __init__(self, app):
        super(RegisterData, self).__init__()
        self.app = app
        self.common = CC.Common(self.app)
        self.listData = LDC.ListData(self.app)

    @htmlPy.Slot(str, result=str)
    def regNewInfo(self, json_data="[]"):
        data = json.loads(json_data)
        if self.common.checkAuth('password', data['masterPassword'], data['username']):
            # Get decrypted intermediary key
            key = self.common.decKey('password', data['masterPassword'], data['username'])
            # Open iv to encrypt data info
            iv = open(os.path.dirname(__file__) + '/../data/security/iv_data_' + str(KEY_LENGTH/2) + '_' + data['username'] + '.txt').read()
            # Open data info file
            df = open(os.path.dirname(__file__) + '/../data/info/' + 'data_enc_' + data['username'] + '_' + str(self.common.genTimestamp()) + '.txt', 'w')
            # Pad data info
            dfPad = self.common.pad(data['infoName'] + '\n' + data['login'] + '\n' + data['password'], len(key))

            # Create the cipher object and process the input stream
            cipher = AES.AESCipher(key, AES.MODE_CBC, iv)

            encData = (iv + cipher.encrypt(dfPad))

            df.write(encData)
            df.close()
            key = None

            # Replace masterPassword to password attr (listInfo requires the masterPassword as password)
            data['password'] = data['masterPassword']
            self.listData.listInfo(data, "")
        else:
            self.listData.listInfo(data, "Wrong master password while adding a new service! Try again.")