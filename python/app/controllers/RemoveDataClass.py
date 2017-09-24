import htmlPy, json, datetime
import os, sys, re, fnmatch
from Crypto.Protocol import KDF
from Crypto.Cipher import AES
import hashlib
import CommonClass as CC
import ListDataClass as LDC

KEY_LENGTH = 32

class RemoveData(htmlPy.Object):

    def __init__(self, app):
        super(RemoveData, self).__init__()
        self.app = app
        self.common = CC.Common(self.app)
        self.listData = LDC.ListData(self.app)

    @htmlPy.Slot(str, result=str)
    def removeInfo(self, json_data="[]"):
        data = json.loads(json_data)
        if(not data['masterPassword']):
            self.listData.listInfo(data, "Wrong master password while removing a service! Try again.")
        elif self.common.checkAuth('password', data['masterPassword'], data['username']):
            # Get decrypted intermediary key
            key = self.common.decKey('password', data['masterPassword'], data['username'])
            # Remove file from respective info
            os.remove(os.path.abspath(__file__ + "/../../data/") + '/info/' + 'data_enc_' + data['username'] + '_' + data['timestamp'] + '.txt')

            key = None

            # Replace masterPassword to password attr (listInfo requires the masterPassword as password)
            data['password'] = data['masterPassword']
            self.listData.listInfo(data, "")
        else:
            self.listData.listInfo(data, "Wrong master password while removing a service! Try again.")