import htmlPy, json
import os, sys
from Crypto.Protocol import KDF
from Crypto.Cipher import AES
import hashlib
import CommonClass as CC
import ListDataClass as LDC

KEY_LENGTH = 32

class Login(htmlPy.Object):

    def __init__(self, app):
        super(Login, self).__init__()
        self.app = app
        self.common = CC.Common(self.app)
        self.listData = LDC.ListData(self.app)

    @htmlPy.Slot()
    def loadLogin(self):
        self.app.template = ("index.html", {})

    @htmlPy.Slot(str, result=str)
    def logUser(self, json_data="[]"):
        data = json.loads(json_data)
        if self.common.checkAuth('password', data['password'], data['username']):
            self.listData.listInfo(data, "")
        else:
            self.app.template = ("index.html", {"error": "User and/or password invalid!"})

    @htmlPy.Slot()
    def logout(self):
        self.app.template = ("index.html", {})